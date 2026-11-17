"""Bounded local video lessons. Captions are not screen observations or truth."""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import struct
from fractions import Fraction
from urllib.parse import urlsplit,parse_qsl

from agent import intelligence_models as im
from agent.intelligence_evidence import HOSTILE
from agent.lab_store import lab_lock
from agent.learning_store import VERSION,capacity,digest,get,load,receipt,run_tool,save,sha,staged
from agent.obsidian import safe_path

LICENSES=('OWN_CREATED','CC0','USER_AUTHORIZED_COPY')
PIPELINE='media-3'


def rights(license,attest):
    if attest is not True or license not in LICENSES:raise PermissionError('explicit rights attestation required; metadata/subtitles cannot authorize access')


def remote(url,license=None,attest=False):
    u=urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.fragment or any(k.casefold() in ('token','key','auth','signature') for k,v in parse_qsl(u.query)):raise ValueError('unsafe source URL')
    allowed=attest is True and license in LICENSES
    return {'state':'BLOCKED','reason':'stage a lawfully obtained local copy; URL/YouTube transport not validated' if allowed else 'rights not attested','URL':url,'network_calls':0,'YouTube':'NOT_VALIDATED','downloaded':False}


def captions(text,duration):
    if len(text.encode())>64000:raise ValueError('caption size cap')
    rows=[]
    pattern=r'(?m)^(?:(\d{2}):)?(\d{2}):(\d{2})[,.](\d{3})\s+-->\s+(?:(\d{2}):)?(\d{2}):(\d{2})[,.](\d{3})[^\n]*\n(.*?)(?=\n\s*\n|\Z)'
    for m in re.finditer(pattern,text,re.S):
        def seconds(parts):
            h,mi,s,ms=parts
            if int(mi)>59 or int(s)>59:raise ValueError('invalid caption timestamp')
            return int(h or 0)*3600+int(mi)*60+int(s)+int(ms)/1000
        start=seconds(m.group(1,2,3,4));end=seconds(m.group(5,6,7,8));body=m[9].strip()
        if not 0<=start<end<=duration+.1 or not body or len(body)>1000:raise ValueError('caption range/content invalid')
        if rows and start<rows[-1]['start_s']:raise ValueError('captions must be ordered')
        rows.append({'id':'caption-'+digest([start,end,body])[:16],'start_s':start,'end_s':end,'text':body,'hostile':bool(HOSTILE.search(body)),'basis':'SUBTITLE_TEXT_ONLY','screen_verified':False})
    if len(rows)>200:raise ValueError('bounded caption window required')
    if text.strip() and not rows:raise ValueError('no supported SRT/VTT cues')
    return rows


def schedule(duration,cues,max_frames,known_times=()):
    if type(max_frames) is not int or not 2<=max_frames<=8 or not math.isfinite(duration) or not 0<duration<=14400:raise ValueError('sampling bounds invalid')
    end=max(0,duration-.05);times={0.0,end}
    for cue in cues:
        if len(times)>=max_frames:break
        if not cue['hostile']:times.add(min(end,cue['start_s']))
    for t in known_times:
        if len(times)>=max_frames:break
        if type(t) in (int,float) and 0<=t<=end:times.add(t)
    i=1
    while len(times)<max_frames and i<max_frames*2:
        times.add(round(end*i/(max_frames-1),6));i+=1
    return sorted(t for t in times if t<=end)


def seek_candidates(requested,duration,fps=None):
    """Container duration is not a decoded frame timestamp. Clamp when a rate
    is reported, otherwise try one earlier bounded seek. Actual PTS, never the
    requested time, is the citation. Missing frames remain explicitly absent.
    """
    if not all(type(v) in (int,float) and math.isfinite(v) for v in (requested,duration)) or not 0<=requested<=duration:raise ValueError('invalid seek time')
    known=type(fps) in (int,float) and math.isfinite(fps) and 0<fps<=240
    first=min(requested,max(0,duration-1/fps)) if known else requested
    earlier=max(0,first-(1/fps if known else 1))
    return list(dict.fromkeys([first,earlier]))


def steps(cues,frames):
    out=[]
    for c in cues:
        matches=[f for f in frames if f.get('asset') and f['observed_pts_s'] is not None and c['start_s']<=f['observed_pts_s']<c['end_s']]
        out.append({'caption_id':c['id'],'start_s':c['start_s'],'end_s':c['end_s'],'statement':c['text'],'basis':'UNTRUSTED_SUBTITLE','status':'QUARANTINED' if c['hostile'] else 'CANDIDATE','frame_refs':[{'asset':f['asset'],'observed_pts_s':f['observed_pts_s']} for f in matches],
                    'operations_mentioned':[w for w in ('select','rotate','keyframe','export','sélectionner','rotation','image clé') if w in c['text'].casefold()] if not c['hostile'] else [],
                    'numeric_literals':re.findall(r'(?<!\w)-?\d+(?:\.\d+)?',c['text'])[:8] if not c['hostile'] else [],'observed_on_screen':[],'inferences':[],'unknown':['actual UI operations/values not verified from pixels','software build and prerequisites unless separately recorded'],'executable':False})
    return out


def probe(root,path,folder):
    binary=shutil.which('ffprobe')
    if not binary:raise RuntimeError('FFprobe unavailable')
    suffix=path.suffix.casefold();fmt={'.mp4':'mov','.mov':'mov','.mkv':'matroska','.webm':'matroska'}[suffix]
    run_tool(root,[binary,'-v','error','-protocol_whitelist','file,pipe','-f',fmt,'-i',str(path),'-show_entries','format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate','-of','json'],folder+'/metadata.json',max_bytes=100000,json_stdout=True)
    m=load(root,folder+'/metadata.json');duration=float(m['format']['duration']);streams=m['streams']
    if not math.isfinite(duration) or not 0<duration<=14400 or len(streams)>16 or not any(s.get('codec_type')=='video' for s in streams):raise ValueError('unsupported video bounds')
    if any(s.get('width',0)>8192 or s.get('height',0)>8192 for s in streams):raise ValueError('video dimensions exceed decoder policy')
    return m,duration,fmt


def compatible_prior(root,spec):
    paths=sorted(safe_path(root,'lab/learning/media').glob('*/result.json'))
    if len(paths)>50:raise ValueError('media cache lookup cap')
    for p in reversed(paths):
        r=get(root,p.parent.relative_to(root).as_posix());old=r.get('spec',{})
        # Only versions with this exact padded PNG decoder pipeline are reusable.
        if old.get('version') not in ('media-2',PIPELINE) or r.get('inputs_obsolete'):continue
        if all(old.get(k)==spec[k] for k in ('input_sha256','captions_sha256','tools')):return r
    return None


def ingest(root,relative,caption_path=None,license='UNKNOWN',attest=False,max_frames=6):
    rights(license,attest);root=Path(root).resolve();video=staged(root,relative,('.mp4','.mov','.mkv','.webm'))
    schedule(1,[],max_frames)
    subtitle=staged(root,caption_path,('.srt','.vtt'),64000) if caption_path else None
    tools={name:{'path':shutil.which(name),'executable_sha256':sha(shutil.which(name))} for name in ('ffmpeg','ffprobe') if shutil.which(name)}
    if len(tools)!=2:raise RuntimeError('FFmpeg and FFprobe required')
    spec={'schema':'vdn.media-spec/1','version':PIPELINE,'tools':tools,'input':relative,'input_sha256':sha(video),'captions':caption_path,'captions_sha256':sha(subtitle) if subtitle else None,'license':license,'rights_attested_by':'explicit local operator','max_frames':max_frames,'audio_window_s':8,'network':False}
    key=digest(spec);folder='lab/learning/media/'+key
    with lab_lock(root,'.learning-media'):
        if safe_path(root,folder+'/result.json').exists():return {**get(root,folder),'cache_hit':True}
        if safe_path(root,folder).exists():raise ValueError('interrupted attempt retained; inspect before explicit revised design')
        def work():
            capacity(root,600000);safe_path(root,folder).mkdir(parents=True);save(root,folder+'/spec.json',spec)
            prior=compatible_prior(root,spec);reused=0
            if prior:
                parent='lab/learning/media/'+prior['key'];shutil.copyfile(safe_path(root,parent+'/metadata.json'),safe_path(root,folder+'/metadata.json'));m=load(root,folder+'/metadata.json');duration=prior['duration_s'];fmt={'.mp4':'mov','.mov':'mov','.mkv':'matroska','.webm':'matroska'}[video.suffix.casefold()]
            else:m,duration,fmt=probe(root,video,folder)
            cues=captions(subtitle.read_text(encoding='utf-8-sig'),duration) if subtitle else []
            cached={f['seek_s']:f for f in prior['frames'] if f.get('asset') and f.get('seek_s') is not None} if prior else {}
            times=schedule(duration,cues,max_frames,cached)
            ff=shutil.which('ffmpeg')
            if not ff:raise RuntimeError('FFmpeg unavailable')
            frames=[];unique={}
            stream=next(s for s in m['streams'] if s['codec_type']=='video');fps=None
            try:
                rate=float(Fraction(stream.get('avg_frame_rate','0/1')))
                if 0<rate<=240 and stream.get('avg_frame_rate')==stream.get('r_frame_rate'):fps=rate
            except (ValueError,ZeroDivisionError):pass
            for i,t in enumerate(times):
                output=safe_path(root,folder+'/sample-'+str(i)+'.png')
                seek=seek_candidates(t,duration,fps)[0]
                if seek in cached:
                    f=cached[seek];asset=f['asset'];shutil.copyfile(safe_path(root,parent+'/'+asset),safe_path(root,folder+'/'+asset));unique[f['sha256']]=asset;frames.append({**f,'requested_s':t,'cached_from':prior['key']});reused+=1;continue
                for attempt,seek in enumerate(seek_candidates(t,duration,fps)):
                    log=folder+'/frame-'+str(i)+'-'+str(attempt)+'.log'
                    run_tool(root,[ff,'-nostdin','-hide_banner','-loglevel','info','-threads','1','-ss',str(seek),'-copyts','-protocol_whitelist','file,pipe','-f',fmt,'-i',str(video),'-map','0:v:0','-vf','scale=256:256:force_original_aspect_ratio=decrease,pad=256:256:(ow-iw)/2:(oh-ih)/2,showinfo','-frames:v','1','-threads','1','-update','1',str(output)],log)
                    if output.exists():break
                if not output.exists():
                    frames.append({'requested_s':t,'observed_pts_s':None,'asset':None,'state':'NO_FRAME_AFTER_BOUNDED_SEEKS'});continue
                header=output.read_bytes()[:24]
                if output.stat().st_size>300000 or not header.startswith(b'\x89PNG\r\n\x1a\n') or len(header)<24 or struct.unpack('>II',header[16:24])!=(256,256):raise ValueError('bounded PNG frame required')
                text=safe_path(root,log).read_text(errors='replace');pts=re.findall(r'pts_time:([0-9.+-]+)',text);observed=float(pts[0]) if pts else None
                h=sha(output);asset='frame-'+h+'.png'
                if h in unique:output.unlink() # only an exact duplicate newly generated in this run
                else:output.rename(safe_path(root,folder+'/'+asset));unique[h]=asset
                frames.append({'requested_s':t,'seek_s':seek,'observed_pts_s':observed,'timestamp_basis':'FFmpeg showinfo with copyts' if pts else 'UNKNOWN','asset':asset,'sha256':h})
            audio={'state':'NO_AUDIO_STREAM','transcription':'NOT_TESTED_NO_SELECTED_LOCAL_MODEL'}
            if any(s.get('codec_type')=='audio' for s in m['streams']):
                output=safe_path(root,folder+'/audio.wav')
                if prior and prior['audio']['state']=='EXTRACTED':shutil.copyfile(safe_path(root,parent+'/audio.wav'),output)
                else:run_tool(root,[ff,'-nostdin','-v','error','-threads','1','-protocol_whitelist','file,pipe','-f',fmt,'-i',str(video),'-map','0:a:0','-t',str(min(8,duration)),'-ac','1','-ar','16000','-c:a','pcm_s16le',str(output)],folder+'/audio.log')
                audio={'state':'EXTRACTED','covered_start_s':0,'covered_end_s':min(8,duration),'sha256':sha(output),'transcription':'NOT_TESTED_NO_SELECTED_LOCAL_MODEL'}
            if sha(video)!=spec['input_sha256'] or subtitle and sha(subtitle)!=spec['captions_sha256']:raise ValueError('input changed during media extraction')
            capacity(root)
            result={'schema':'vdn.media-result/1','key':key,'state':'PARTIAL','spec':spec,'duration_s':duration,'frames':frames,'reused_frames':reused,'parent_key':prior['key'] if prior else None,'unique_images':len(unique),'steps':steps(cues,frames),'audio':audio,'vision':{'state':'NOT_TESTED_NO_SELECTED_INSTALLED_MODEL','observations':[]},'YouTube':'NOT_VALIDATED','truth_verified':False,'cache_hit':False,'scope':'Actual local decoding and literal captions; no autonomous visual understanding, source truth or Blender execution inferred.'}
            return receipt(root,folder,result)
        try:return im.operation(root,work)
        except Exception as exc:
            from agent.reliability import BlackBox
            BlackBox(root).incident('media','local_ingest',str(exc),'MEDIUM',type(exc).__name__,True);raise


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--input',required=True);p.add_argument('--captions');p.add_argument('--license',default='UNKNOWN');p.add_argument('--attest-rights',action='store_true');a=p.parse_args()
    try:
        r=remote(a.input,a.license,a.attest_rights) if a.input.startswith('https:') else ingest(a.root,a.input,a.captions,a.license,a.attest_rights)
        print(json.dumps(r,ensure_ascii=False,indent=2));return 2 if r.get('state')=='BLOCKED' else 0
    except (OSError,ValueError,RuntimeError) as exc:print(json.dumps({'state':'BLOCKED','type':type(exc).__name__}));return 2


if __name__=='__main__':raise SystemExit(main())
