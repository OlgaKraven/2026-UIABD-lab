from pathlib import Path
import json,zipfile
from decimal import Decimal
from lxml import etree
R=Path(__file__).resolve().parents[1]
def fmt(n):return str(n).replace('.',',')
payload=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))
original=json.loads((R/'authoring/original-labs.json').read_text(encoding='utf-8-sig'))
original={l['id']:l for l in original}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for lab in payload['labs']:
 points=(3 if lab['number']<=3 else 4) if lab['semester']==6 else 2.5 if lab['semester']==7 else 10
 old_points=lab['points'];lab['points']=points
 for criterion,source in zip(lab['rubric'],original[lab['slug']]['lms']['rubric']):
  criterion['points']=float(Decimal(str(source['points']))*Decimal(str(points))/10)
  if criterion['points'].is_integer():criterion['points']=int(criterion['points'])
 if old_points==points:continue
 p=R/'public/reports'/lab['reportFile']
 with zipfile.ZipFile(p) as z:files={n:z.read(n) for n in z.namelist()}
 root=etree.fromstring(files['word/document.xml'])
 for t in root.xpath('//w:t',namespaces=ns):
  if t.text and 'максимум ' in t.text:t.text=t.text.replace(f'максимум {old_points} баллов',f'максимум {fmt(points)} балла')
 tables=root.xpath('//w:tbl',namespaces=ns);updated=0
 for table in tables:
  rows=table.xpath('./w:tr',namespaces=ns)
  if not rows or ''.join(rows[0].xpath('.//w:t/text()',namespaces=ns))!='РезультатБаллы':continue
  for row,criterion in zip(rows[1:],lab['rubric']):
   texts=row.xpath('./w:tc[2]//w:t',namespaces=ns);texts[0].text=fmt(criterion['points'])
   for t in texts[1:]:t.text=''
  updated+=1
 assert updated==1,lab['slug']
 files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in files.items():z.writestr(n,b)
(R/'src/data/labs.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated points and 17 report templates; totals:',{s:sum(l['points'] for l in payload['labs'] if l['semester']==s) for s in [6,7,8]})
