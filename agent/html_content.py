"""Extract article content before truncation; navigation is not evidence."""
from html.parser import HTMLParser
import re


def article_text(html):
    class Parser(HTMLParser):
        def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.main=[];self.fallback=[];self.found=False
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs);parent=self.stack[-1] if self.stack else ('',False,False);blocked=parent[1] or tag in ('script','style','nav','footer') or attrs.get('role') in ('navigation','banner','contentinfo');active=parent[2] or tag in ('main','article') or attrs.get('role')=='main'
            if active and not blocked:self.found=True
            if tag not in ('br','hr','img','meta','link','input','source','wbr'):self.stack.append((tag,blocked,active))
            if tag in ('p','div','section','li','h1','h2','h3','pre','br'):self.handle_data('\n')
        def handle_endtag(self,tag):
            for i in range(len(self.stack)-1,-1,-1):
                if self.stack[i][0]==tag:del self.stack[i:];break
            if tag in ('p','div','section','li','h1','h2','h3','pre'):self.handle_data('\n')
        def handle_data(self,text):
            _,blocked,active=self.stack[-1] if self.stack else ('',False,False)
            if not blocked:
                self.fallback.append(text)
                if active:self.main.append(text)
    p=Parser();p.feed(html);text=''.join(p.main if p.found else p.fallback);return re.sub(r'\n[ \t\n]+','\n\n',text).strip()


def navigation_capture(text):
    """Conservative signature of observed Sphinx navigation-only truncation.

    This is a review flag, not semantic source validation. Retain the receipt.
    """
    return text[:32000].lower().count('toggle navigation') >= 5
