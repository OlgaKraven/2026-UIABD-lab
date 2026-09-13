from pathlib import Path
import json,csv,io
R=Path(__file__).resolve().parents[1]
labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs']
windows=[('09:12','09:16'),('10:00','10:04'),('11:42','11:44'),('13:06','13:07'),('14:21','14:22'),('15:34','15:35')]
rows=[]
for v in range(1,31):
 start,end=windows[(v-1)%6];rows.append([f'W{v:02}',v,'2026-02-12T'+start+':00Z','2026-02-12T'+end+':00Z'])
with (R/'inputs/incidents/log-windows.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['window_id','variant','from','to']);w.writerows(rows)
for l in labs:
 l['sourceData']['sections'].insert(0,{'title':'Как запустить и проверить стенд','content':[(R/'inputs/docs/stand-start.md').read_text(encoding='utf-8')]})
 l['standFiles'].append('inputs/docs/stand-start.md')
 for s in l['sourceData']['sections']:
  if s['title']=='log-windows.csv':s['table']={'columns':['window_id','variant','from','to'],'rows':rows};s['content']=['Окна относятся к записям предоставленного журнала. Время UTC; границы включены. Выберите строку своего варианта.']
(R/'src/data/labs.json').write_text(json.dumps({'labs':labs},ensure_ascii=False,indent=2),encoding='utf-8')
print('Corrected 30 log windows and linked stand instructions')
