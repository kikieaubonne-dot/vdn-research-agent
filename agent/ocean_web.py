"""Bounded public-web discovery atop V10 transport, cache and robots policy.

DNS is checked at connection time and the connection is pinned to a public IP.
No proxy, authentication, private addresses or cross-origin redirects.
"""
import datetime as dt
import hashlib
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import socket
import time
from urllib.parse import urlparse,urljoin,parse_qsl
from urllib.request import HTTPSHandler,ProxyHandler,build_opener,getproxies,proxy_bypass
from urllib.robotparser import RobotFileParser
from agent import providers,budget
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.storage import atomic_write
from agent.text import tokens


def settings(root):
    path=safe_path(root,'config/ocean.json')
    if path.stat().st_size>100000:raise ValueError('oversized Ocean configuration')
    cfg=json.loads(path.read_text(encoding='utf-8'));clean_json(cfg,100000)
    if cfg.get('schema')!='vdn.ocean-config/11' or type(cfg['enabled']) is not bool:raise ValueError('invalid Ocean configuration')
    if cfg.get('network_mode','direct_public') not in ('direct_public','trusted_system_proxy') or type(cfg.get('trust_system_proxy',False)) is not bool:raise ValueError('invalid transport mode')
    if cfg.get('network_mode')=='trusted_system_proxy' and not cfg.get('trust_system_proxy'):raise ValueError('system proxy requires explicit operator trust')
    if cfg['model_backend'] not in ('none','local','remote') or type(cfg['semantic']['enabled']) is not bool:raise ValueError('invalid model settings')
    for key in ('storage_bytes','min_free_bytes','cache_ttl_s','max_document_bytes','max_links','sources_per_unit','max_model_calls'):
        if type(cfg[key]) is not int or cfg[key]<0:raise ValueError('invalid Ocean limit: '+key)
    if not 1<=cfg['sources_per_unit']<=4 or not 1<=cfg['max_links']<=100 or not 1024<=cfg['max_document_bytes']<=3000000:raise ValueError('unsafe document/link limits')
    for key in ('max_cost_usd','remote_reservation_usd'):
        if type(cfg[key]) not in (int,float) or cfg[key]<0:raise ValueError('invalid cost budget')
    for spec in cfg['providers'].values():
        if type(spec['enabled']) is not bool or not isinstance(spec['hosts'],list) or not spec.get('policy'):raise ValueError('provider permission/policy required')
        if len(spec['seeds'])>5 or not all(re.fullmatch(r'[a-z0-9.-]+',h) and '.' in h for h in spec['hosts']):raise ValueError('invalid provider host/seed list')
        for seed in spec['seeds']:
            providers.validate_url(seed,spec['hosts'])
            p=urlparse(seed)
            if p.fragment or any(k.lower() in ('token','key','auth','signature','access_token') for k,v in parse_qsl(p.query)):raise ValueError('unsafe provider seed')
    return cfg


def public_addresses(host):
    try:ipaddress.ip_address(host);raise ValueError('IP literals not permitted')
    except ValueError as exc:
        if str(exc)=='IP literals not permitted':raise
    rows=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    addresses=list(dict.fromkeys(r[4][0] for r in rows))
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):raise ValueError('non-public DNS address refused')
    budget.check();return addresses


class PublicConnection(http.client.HTTPSConnection):
    def connect(self):
        if self._tunnel_host:raise ValueError('proxy tunnel refused')
        addresses=public_addresses(self.host)
        # Pin the selected address; do not resolve the hostname a second time.
        last=None
        candidates=[a for a in addresses if ':' not in a][:2]+[a for a in addresses if ':' in a][:2]
        for address in candidates:
            budget.check();active=budget.CURRENT.get()
            remaining=max(.001,active.deadline-time.monotonic()) if active else self.timeout
            try:raw=socket.create_connection((address,443),min(self.timeout,remaining),self.source_address)
            except OSError as exc:last=exc;continue
            try:self.sock=self._context.wrap_socket(raw,server_hostname=self.host);return
            except BaseException:raw.close();raise
        raise last or OSError('no public address available')


class PublicHTTPS(HTTPSHandler):
    def https_open(self,req):return self.do_open(PublicConnection,req,context=self._context)


class OceanWeb:
    def __init__(self,root,opener=None):
        self.root=Path(root).resolve();self.cfg=settings(root);self.robot_rules={};self.raw_opener=opener
        self.purpose='content';self.cache_hits=0;self.successful_responses=0

    def path(self,relative):return safe_path(self.root,'lab/ocean/'+relative)

    def storage_check(self,extra=0):
        total=0;count=0
        for folder in (self.root/'lab/ocean',self.root/'knowledge/ocean'):
            for p in folder.rglob('*') if folder.exists() else []:
                if p.is_file():
                    safe_path(self.root,p.relative_to(self.root).as_posix());count+=1;total+=p.stat().st_size
                    if count>10000:raise ValueError('Ocean file count limit exceeded')
        if total+extra>self.cfg['storage_bytes']:raise budget.BudgetExhausted('Ocean storage budget',scope='library',resource='storage_bytes',limit=self.cfg['storage_bytes'],used=total)
        if shutil.disk_usage(self.root).free<self.cfg['min_free_bytes']:raise ValueError('insufficient free disk space')

    def trace(self,kind,url=None,**fields):
        event={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'kind':kind,'purpose':self.purpose,**fields}
        if url:event['url']=providers.canonical_url(url)
        text=clean_json(event)+'\n';self.storage_check(len(text.encode('utf-8')))
        p=self.path('web-trace.jsonl');p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('a',encoding='utf-8') as f:f.write(text);f.flush();os.fsync(f.fileno())

    def allowed(self,url,spec):
        p=urlparse(url)
        if (p.hostname or '').lower() not in spec['hosts'] or p.fragment or any(k.lower() in ('token','key','auth','signature','access_token') for k,v in parse_qsl(p.query)):
            raise providers.FetchError('URL outside provider permission')
        clean_json({'url':url})
        providers.validate_url(url,spec['hosts'])
        return p.hostname.lower()

    def _open(self,req,timeout):
        self.trace('http_attempt',req.full_url,network_mode=self.cfg.get('network_mode','direct_public'))
        try:
            result=(self.raw_opener or self.opener.open)(req,timeout=timeout)
            self.successful_responses+=1
            self.trace('http_response',req.full_url,status=getattr(result,'status',200))
            return result
        except providers.HTTPError as exc:
            self.trace('http_error',req.full_url,status=exc.code);raise
        except (OSError,ValueError,providers.URLError) as exc:
            self.trace('transport_error',req.full_url,error_kind=type(exc).__name__);raise

    def _fetch(self,url,spec,purpose,max_bytes):
        host=self.allowed(url,spec);outer=self
        class Redirect(providers.CheckedRedirect):
            def redirect_request(self,req,fp,code,msg,headers,newurl):
                if outer.allowed(newurl,spec)!=host:raise providers.FetchError('cross-origin redirect refused')
                if purpose!='robots' and not outer.robot_rules[host].can_fetch(providers.USER_AGENT,newurl):raise providers.FetchError('redirect blocked by robots')
                result=super().redirect_request(req,fp,code,msg,headers,newurl)
                if result is not None:outer.trace('redirect_attempt',newurl)
                return result
        if self.cfg.get('network_mode')=='trusted_system_proxy':
            # The operator trusts this proxy to enforce destination policy. Honor
            # its inherited routes/CA, never print or persist proxy credentials.
            if not getproxies().get('https') or proxy_bypass(host):raise ValueError('no configured proxy route for source')
            public_addresses(host)
            self.opener=build_opener(ProxyHandler(),HTTPSHandler(),Redirect())
        else:self.opener=build_opener(ProxyHandler({}),PublicHTTPS(),Redirect())
        self.purpose=purpose
        return providers.http_get(url,max_bytes=max_bytes,retries=1,allow_extra_hosts=spec['hosts'],opener=self._open,use_env_auth=False)

    def robots(self,url,spec):
        host=self.allowed(url,spec)
        if host not in self.robot_rules:
            robots_url='https://'+host+'/robots.txt'
            cached=self.path('robots/'+hashlib.sha256(host.encode()).hexdigest()+'.json')
            record=json.loads(cached.read_text(encoding='utf-8')) if cached.exists() else None
            if not record or time.time()-record['at']>self.cfg['cache_ttl_s']:
                try:text=self._fetch(robots_url,spec,'robots',16000);decision='parsed'
                except providers.FetchError as exc:
                    if exc.status!=404:raise # auth, rate limits, anti-bot and server failures are not bypassed
                    text='User-agent: *\nAllow: /\n';decision='robots_404_allow_RFC9309'
                if re.search(r'(?i)<html|<body|captcha|access denied',text) or (text.strip() and not re.search(r'(?im)^(?:user-agent|sitemap)\s*:',text) and not all(s.lstrip().startswith('#') for s in text.splitlines() if s.strip())):raise providers.FetchError('invalid robots response; source refused')
                record={'at':time.time(),'text':text,'decision':decision,'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}
                encoded=clean_json(record);self.storage_check(len(encoded.encode('utf-8')));atomic_write(cached,encoded)
            if hashlib.sha256(record['text'].encode('utf-8')).hexdigest()!=record.get('sha256'):raise ValueError('robots cache integrity failure')
            parser=RobotFileParser();parser.parse(record['text'].splitlines());self.robot_rules[host]=parser
        if not self.robot_rules[host].can_fetch(providers.USER_AGENT,url):raise providers.FetchError('robots policy refused source')

    def get(self,url,provider,purpose='content'):
        spec=self.cfg['providers'].get(provider)
        if not spec or not spec['enabled']:raise providers.FetchError('provider disabled')
        self.allowed(url,spec);self.storage_check()
        if re.search(r'(?i)\.(?:png|jpe?g|gif|webp|svg|mp4|webm|zip|exe|fbx|blend|pdf|css|js)$',urlparse(url).path):raise providers.FetchError('non-document asset refused')
        path=self.path('sources/'+hashlib.sha256(url.encode()).hexdigest()+'.json')
        old=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
        if old and time.time()-old['at']<=self.cfg['cache_ttl_s']:
            if old['url']!=providers.canonical_url(url) or old['provider']!=provider or hashlib.sha256(old['text'].encode('utf-8')).hexdigest()!=old['text_sha256']:raise ValueError('source cache integrity failure')
            self.cache_hits+=1;self.purpose=purpose;self.trace('cache_hit',url);return {**old,'cached':True}
        self.robots(url,spec)
        raw=self._fetch(url,spec,purpose,self.cfg['max_document_bytes'])
        html=bool(re.search(r'(?i)<(?:html|body|article)\b',raw))
        text=providers.strip_html(raw) if html else raw
        if len(text.strip())<80:raise providers.FetchError('empty or insufficient source content')
        if re.search(r'(?i)captcha|access denied|verify you are human|sign in to (?:access|continue|view)|subscription required',text[:2000]):raise providers.FetchError('access challenge refused')
        links=[]
        patterns=re.findall(r'(?i)href=["\x27]([^"\x27]+)["\x27]',raw) if html else re.findall(r'\]\(([^\s)]+)',raw)
        for link in patterns:
            target=urljoin(url,link).split('#')[0]
            try:self.allowed(target,spec)
            except (ValueError,providers.FetchError):continue
            if re.search(r'(?i)\.(?:png|jpe?g|gif|webp|svg|mp4|webm|zip|exe|fbx|blend|pdf|css|js)$',urlparse(target).path):continue
            if urlparse(target).hostname=='create.roblox.com' and urlparse(target).path.startswith('/docs/') and not Path(urlparse(target).path).suffix:
                target=target.rstrip('/')+'.md'
            if target not in links:links.append(target)
            if len(links)>=self.cfg['max_links']:break
        published=re.search(r'(?is)<meta[^>]+(?:property|name)=["\x27](?:article:published_time|datePublished)["\x27][^>]+content=["\x27](\d{4}-\d{2}-\d{2})',raw)
        record={'url':providers.canonical_url(url),'provider':provider,'at':time.time(),
                'accessed':dt.datetime.now(dt.timezone.utc).date().isoformat(),'published':published.group(1) if published else None,'version':'unknown',
                'text':text.encode('utf-8')[:32000].decode('utf-8','ignore'),'truncated':len(text.encode('utf-8'))>32000,'policy':spec['policy'],'links':links,
                'raw_text_sha256':hashlib.sha256(raw.encode('utf-8')).hexdigest(),
                'changed_since_previous':bool(old and old['raw_text_sha256']!=hashlib.sha256(raw.encode('utf-8')).hexdigest())}
        record['text_sha256']=hashlib.sha256(record['text'].encode('utf-8')).hexdigest()
        encoded=clean_json(record);self.storage_check(len(encoded.encode('utf-8')));atomic_write(path,encoded)
        self.trace('source_cached',url,extracted_utf8_bytes=len(record['text'].encode('utf-8')),truncated=record['truncated'])
        return {**record,'cached':False}

    def discover(self,provider,query):
        spec=self.cfg['providers'].get(provider)
        if not spec or not spec['enabled']:return []
        candidates=[];words=set(tokens(query))
        seeds=spec['seeds']
        if provider=='github':
            from urllib.parse import quote
            seeds=['https://api.github.com/search/repositories?q='+quote(query+' is:public')+'&per_page=5']
        for seed in seeds[:2]:
            record=self.get(seed,provider,'discovery')
            if provider=='github':
                data=json.loads(record['text']);candidates += [x['html_url'] for x in data.get('items',[]) if x.get('private') is False]
            else:candidates += [seed]+record['links']
        unique=list(dict.fromkeys(candidates))
        unique.sort(key=lambda u:(-len(words&set(tokens(u))),u))
        return unique[:self.cfg['max_links']]
