"""Validate HTML links, fragment targets, CSS assets, and slideshow images offline.
Usage: python tools/validate.py [site-root]
Python standard library only. No installation or network required.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import re,json,sys

class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('name'):self.ids.add(a['name'])
  for key in ('href','src','poster','data-src','data-original','background'):
   if a.get(key):self.refs.append((a[key],tag+'/'+key))
  if a.get('srcset'):
   self.refs.extend((v.strip().split()[0],'srcset') for v in a['srcset'].split(','))
  if a.get('style'):self.refs.extend((x,'css') for x in cssrefs(a['style']))
def cssrefs(text):
 return [m[1] for m in re.findall(r'url\(\s*([\'\"]?)(.*?)\1\s*\)',text,re.I)]+re.findall(r'@import\s+[\'\"]([^\'\"]+)',text,re.I)
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
pages={p:Page(p.read_text(encoding='utf-8')) for p in root.glob('*.html')}
missing=[];fragments=[];external=[];checked=0
for p in list(pages)+list((root/'files').rglob('*.css'))+list((root/'assets').rglob('*.css')):
 text=p.read_text(encoding='utf-8');refs=list(pages[p].refs) if p in pages else []
 refs.extend((r,'css') for r in cssrefs(text))
 if p in pages:
  refs.extend(('/uploads/'+r.replace('\\/','/'),'slideshow') for r in re.findall(r'"url"\s*:\s*"(2[^"\s]+)"',text))
 for ref,kind in refs:
  if ref.startswith(('data:','mailto:','tel:','javascript:')):continue
  u=urlsplit(urljoin('https://local.test/'+p.relative_to(root).as_posix(),ref))
  if u.netloc not in ('local.test','robots.iit.edu','www.robots.iit.edu'):
   external.append({'page':p.relative_to(root).as_posix(),'url':ref,'kind':kind});continue
  dest=root/unquote(u.path).lstrip('/')
  if u.path.endswith('/'):dest=dest/'index.html'
  checked+=1
  if not dest.is_file():missing.append({'page':p.relative_to(root).as_posix(),'reference':ref,'kind':kind})
  elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:
   fragments.append({'page':p.relative_to(root).as_posix(),'reference':ref})
report={'pages':len(pages),'references_checked':checked,'missing_files':missing,'missing_fragments':fragments,'external_references':external}
out=root/'_migration/link-check.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='external_references'},indent=2))
sys.exit(bool(missing or fragments))
