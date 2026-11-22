from pathlib import Path
import requests,json,re,concurrent.futures
R=Path(__file__).resolve().parents[1]; O=R/'artifacts/md-details-research'; O.mkdir(parents=True,exist_ok=True)
terms=['Topstitch','Binding','Puckering','Button','Buttonhole','Fasten','Pocket','Zipper','Elastic','Pressure','Fold Angle','Layer Clone','Strengthen','Shrinkage','Tack','Piping','Offset as Internal Line']
def work(q):
 r=requests.get('https://support.marvelousdesigner.com/api/v2/help_center/articles/search.json',params={'query':q,'locale':'en-us','per_page':8},timeout=40);r.raise_for_status()
 aa=r.json()['results']; out=[]
 for a in aa:
  if a.get('locale')!='en-us':continue
  (O/(str(a['id'])+'.json')).write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
  out.append((a['id'],a['title']))
 return q,out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for x in pool.map(work,terms):print(x)
