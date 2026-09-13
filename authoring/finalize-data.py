from pathlib import Path
import json,re,csv,io
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def dump(p,v):(R/p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
labs=load('src/data/labs.json')['labs'];ds=load('src/data/datasets.json');method=load('authoring/methodology.json')
for l in labs:
 for s in l['sourceData']['sections']:
  if 'content' in s:s['content']=[re.sub(r' — ориентир \d+ минут','',x) for x in s['content']]
  if s['title']=='service_ops_schema.sql':s['content'].insert(0,'Запускайте только при создании новой пустой базы. Не выполняйте повторно поверх готовых таблиц. Код в файлах с обозначениями :параметр и комментариями-заготовками нужно дополнить перед запуском; это задания, а не готовое решение.')
 for v in range(1,31):
  dataset=ds[l['slug']][str(v)]
  if l['slug']=='C4_S7_LR06':
   records=[]
   for n in range(24):
    material=1+(v+n)%4;branch=1+(v+n)%3;quantity=[1+v%5,0,999999,-1,2,3][n%6];typ=['RECEIPT','ISSUE'][n%2]
    ref=f'V{v:02}-P{n+1:02}' if n%6!=5 else f'V{v:02}-P{n:02}'
    records.append([f'P{n+1:02}',material,branch,quantity,typ,ref,'',''])
   dataset['sections']=[{'title':'procedure_cases.csv','content':['До каждой независимой группы сохраните исходный остаток. Запуски внутри группы по 6 строк выполняйте по порядку; группы изолируйте транзакцией или новой учебной копией. При повторе reference_no сохраните результат первого вызова. Не запускайте все вызовы без анализа ошибок.'],'table':{'columns':['test_id','material_id','branch_id','quantity','movement_type','reference_no','Ожидается до запуска','Фактически'],'rows':records}}]
  if l['slug']=='C4_S7_LR07':
   records=[]
   for n in range(24):
    records.append([f'T{n+1:02}',1001+(v+n-1)%30,['NEW','IN_PROGRESS','DONE','CANCELLED'][(v+n)%4],'ROLLBACK' if n%3==0 else 'COMMIT','',''])
   dataset['sections']=[{'title':'audit_cases.csv','content':['Перед каждой строкой получите текущий статус и число строк аудита. Выполняйте UPDATE в отдельной транзакции; завершение указано в столбце finish. Запишите ожидаемое изменение до запуска и фактическое число записей после завершения.'],'table':{'columns':['test_id','order_id','new_status','finish','Ожидаемое изменение','Фактическое изменение'],'rows':records}}]
  if l['slug']=='C4_S7_LR05':
   records=[]
   for n in range(24):records.append([f'B{n+1:02}',1001+(n+v-1)%30,['исходный заказ','без позиций услуг','нет нормы материала','дробное количество','отсутствующий заказ','нулевая цена'][n%6],'','',''])
   dataset['sections']=[{'title':'boundary_cases.csv','content':['Исходные заказы не меняйте: создайте временные копии или выполняйте изменения в транзакции с откатом. Для каждого случая укажите фактическое преобразование входа. Нулевую цену и дробное количество проверяйте только там, где схема допускает их.'],'table':{'columns':['test_id','source_order_id','Условие','Изменение входа','Ожидаемый итог','Фактический итог'],'rows':records}}]
  # Generic client-side variant resolution also selects rows in multi-variant source tables.
 if l['slug'] in ['C4_S7_LR05','C4_S7_LR06','C4_S7_LR07'] or (l['semester']==8 and l['number']<5):
  action='Выполните проверки нового набора своего варианта. Для каждой записи сначала сформулируйте ожидаемый результат, затем зафиксируйте наблюдение и объясните расхождение.'
  if action not in l['task']:
   l['task'].append(action);method[l['slug']]['steps'].append({'data':'Дополнительная таблица своего варианта в разделе данных.','result':'Итоги по всем ID; команды и подробный разбор одного обычного и одного граничного случая.','check':'Каждый ID имеет результат либо обоснованную причину невозможности проверки. Учебные измерения не названы измерениями собственной системы.'})
 for s in l['sourceData']['sections']:
  if s['title']=='connection-cases.json':
   # Remove answer fields already stripped by enrichment; retained source is separate.
   s['content'][0]=re.sub(r'(?i)service is not running','connection refused',s['content'][0])
dump('src/data/labs.json',{'labs':labs});dump('src/data/datasets.json',ds);dump('authoring/methodology.json',method)
(R/'src/data/methodology.ts').write_text('export interface StepGuide {data:string;result:string;check:string}\nexport const labMethodology:Record<string,{sequence:{previous:string;next:string};example:{title:string;source:string;method:string[];result:string;boundary:string};steps:StepGuide[]}> = '+json.dumps(method,ensure_ascii=False,indent=2),encoding='utf-8')
for p in (R/'inputs/demo-exam').glob('*.md'):p.write_text(re.sub(r' — ориентир \d+ минут','',p.read_text(encoding='utf-8-sig')),encoding='utf-8')
print('Variant checks and student text updated')
