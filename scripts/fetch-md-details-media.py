from pathlib import Path
import requests,json,re
R=Path(__file__).resolve().parents[1];D=R/'content/assets/md-details';D.mkdir(parents=True,exist_ok=True)
manifest=[]
for aid,name in [(47358128286617,'topstitch'),(47358111713817,'puckering'),(47358121260441,'button')]:
 a=requests.get(f'https://support.marvelousdesigner.com/api/v2/help_center/en-us/articles/{aid}.json',timeout=40).json()['article']
 (R/'artifacts/md-details-research'/f'{aid}.json').write_text(json.dumps(a,ensure_ascii=False),encoding='utf-8')
 urls=list(dict.fromkeys(re.findall(r'<img[^>]+src=[\x22\x27]([^\x22\x27]+)',a['body'])))
 for i,u in enumerate(urls):
  if not u.startswith('https://support.marvelousdesigner.com/'):continue
  r=requests.get(u,timeout=40);r.raise_for_status()
  if len(r.content)<8000:continue
  ext='.png' if 'png' in r.headers.get('content-type','') else '.jpg'
  f=f'{name}-{i}{ext}';(D/f).write_bytes(r.content)
  manifest.append({'file':f,'source':a['html_url'],'imageUrl':u,'credit':'Marvelous Designer Help Center','accessed':'2026-11-21'})
  print(f,len(r.content))
(R/'content/md-details-media-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
