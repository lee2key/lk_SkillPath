from pathlib import Path
import json,xml.etree.ElementTree as ET,html,base64
R=Path(__file__).resolve().parents[1]
before=json.loads((R/'artifacts/md-before-details.json').read_text(encoding='utf-8'))
after=json.loads((R/'content/courses.json').read_text(encoding='utf-8'))
b=before['courses'][0];a=after['courses'][0]
assert a['lessons'][:len(b['lessons'])]==b['lessons'],'Original lessons changed'
new=[l for l in a['lessons'] if l['id'].startswith('md-details-ru-')]
assert len(new)==20
assert len({l['id'] for l in a['lessons']})==len(a['lessons'])
rows=[]
for l in new:
 assert any(x.get('media') for x in l['blocks'])
 for block in l['blocks']:
  if block['type']=='choice':assert 0<=block['answer']<len(block['options'])
  if block.get('media'):
   p=R/block['media'].lstrip('/');assert p.is_file()
   if p.suffix=='.svg':ET.parse(p)
   mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
   url=f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode()
   rows.append('<section><h2>'+html.escape(l['title'])+'</h2><img src="'+url+'"><p>'+html.escape(block['text'])+'</p></section>')
out='<meta charset="utf-8"><title>MD — проверка новых уроков</title><style>body{font:16px Segoe UI;background:#edf1f3;margin:24px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}section{background:white;padding:20px;border-radius:14px}h2{font-size:20px}img{width:100%;max-height:400px;object-fit:contain}p{white-space:pre-line;overflow-wrap:anywhere}</style><main>'+''.join(rows)+'</main>'
(R/'artifacts/md-details-review.html').write_text(out,encoding='utf-8')
print('PASS: 20 new lessons, original lessons unchanged, images and quiz answers valid')
