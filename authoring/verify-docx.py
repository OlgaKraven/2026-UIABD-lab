from pathlib import Path
import zipfile,json,re,hashlib
from docx import Document
from docx.oxml.ns import qn
R=Path(__file__).resolve().parents[1];labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs'];out=[]
for l in labs:
 p=R/'public/reports'/l['reportFile'];d=Document(p)
 with zipfile.ZipFile(p) as z:
  assert all(b'TargetMode="External"' not in z.read(n) for n in z.namelist() if n.endswith('.rels'))
  xml=z.read('word/document.xml').decode();assert l['title'] in ''.join(d._element.xpath('//w:t/text()'))
  assert 'durationAcademicHours' not in xml and not re.search('ориентир [0-9]+ минут',xml)
  for sz in d._element.xpath('//w:rPr/w:sz'):assert sz.get(qn('w:val'))=='24'
  assert not d._element.xpath('//w:trHeight[@w:hRule="exact"]')
 out.append({'id':l['slug'],'editable':True,'externalLinks':0,'fontPt':12,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'quality/docx-check.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('22 DOCX checked')
