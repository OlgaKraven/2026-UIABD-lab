from pathlib import Path
import zipfile,json,csv,io,hashlib,re
R=Path(__file__).resolve().parents[1];W=R.parent
labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs'];results=[]
originals=json.loads((R/'authoring/original-variants.json').read_text(encoding='utf-8'))
for scope in ['6','7','8','all']:
 selected=[l for l in labs if scope=='all' or str(l['semester'])==scope];p=W/f'lab-{scope}.zip'
 with zipfile.ZipFile(p) as z:
  names=z.namelist();htmls=[n for n in names if n.endswith('Начните_здесь.html')];assert len(htmls)==len(selected)*30,(scope,len(htmls))
  for lab in selected:
   for v in range(1,31):
    prefix=f'V{v:02}/ЛР{lab["slug"]}/';html=z.read(prefix+'Начните_здесь.html').decode('utf-8')
    assert lab['title'] in html and f'V{v:02}' in html
    assert f'Критерии оценки · {lab["points"]} баллов' in html,(lab['slug'],v,'wrong points in HTML')
    assert originals['inputs/demo-exam/kod-5-variants.csv']['rows'][v-1]['enterprise_profile'] in html
    matrix=originals[f'inputs/variants/{"c3" if lab["semester"]==6 else "c4"}-s{lab["semester"]}-variants.csv']['rows'][v-1]
    conditions=list(csv.reader(io.StringIO(z.read(prefix+'Данные/Условия_варианта.csv').decode('utf-8-sig')),delimiter=';'))
    actual={row[1]:row[2] for row in conditions[1:]}
    assert all(actual.get(k)==value for k,value in matrix.items()),(lab['slug'],v,'original conditions mismatch')
    assert not re.search(r'<(?:script|link|button)\b',html)
    assert not re.search(r'https?://[^\s<"]*lecture',html,re.I)
    assert not re.search(r'ориентир \d+ минут|durationAcademicHours|private/qa',html)
    doc=z.read(prefix+'Шаблон_для_заполнения.docx');assert hashlib.sha256(doc).digest()==hashlib.sha256((R/'public/reports'/lab['reportFile']).read_bytes()).digest()
    with zipfile.ZipFile(io.BytesIO(doc)) as dz:
     xml=''.join(dz.read(n).decode('utf-8') for n in dz.namelist() if n.endswith('.xml'))
     assert not re.search(r'https?://[^<\s"]*lecture',xml,re.I)
     for rel in [n for n in dz.namelist() if n.endswith('.rels')]:assert b'TargetMode="External"' not in dz.read(rel)
    csvs=[n for n in names if n.startswith(prefix+'Данные/') and n.endswith('.csv')];assert len(csvs)>=2
    for name in csvs:
     raw=z.read(name);assert raw.startswith(b'\xef\xbb\xbf');rows=list(csv.reader(io.StringIO(raw.decode('utf-8-sig')),delimiter=';'));assert all(len(row)==len(rows[0]) for row in rows)
     if 'variant' in rows[0]:assert all(int(row[rows[0].index('variant')])==v for row in rows[1:])
    if lab['slug']=='C4_S8_LR05':
     content=json.loads(z.read(prefix+'Стенд/demo-exam/kod-5-customers.json'));assert set(content['variants'])=={f'{v:02}'}
  results.append({'scope':scope,'sets':len(htmls),'bytes':p.stat().st_size,'status':'passed'})
(R/'quality/archive-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
