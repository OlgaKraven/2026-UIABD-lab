from pathlib import Path
import subprocess,json,csv,io,re
R=Path(__file__).resolve().parents[1]
labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs']
ds=json.loads((R/'src/data/datasets.json').read_text(encoding='utf-8'))
def query(sql):
 p=subprocess.run(['docker','exec','uiabd-lab-qa-20260913','mysql','-uroot','uiabd_qa','--batch','--raw','-e',sql],capture_output=True,check=True)
 return list(csv.reader(p.stdout.decode('utf-8').splitlines(),delimiter='\t'))
tables={}
for table in ['branches','customers','services','materials','material_norms','orders','order_items','material_balances']:
 extra=' WHERE order_id < 100000' if table in ['orders','order_items'] else ''
 tables[table]=query(f'SELECT * FROM {table}'+extra)
sqljobs=['C3_S6_LR03','C3_S6_LR04','C4_S7_LR01','C4_S7_LR02','C4_S7_LR03','C4_S7_LR04','C4_S7_LR05','C4_S7_LR06','C4_S7_LR07','C4_S7_LR08','C4_S7_LR09']
for l in labs:
 if l['slug'] in sqljobs:
  for name,rows in tables.items():
   if any(s['title']==name+'.csv' for s in l['sourceData']['sections']):continue
   l['sourceData']['sections'].append({'title':name+'.csv','content':['Табличная копия исходного состояния SQL-стенда для сверки и обработки. Цены — рубли за единицу; количество — единицы услуги либо материала. ID связывают одноимённые ключи таблиц. Время created_at — техническое поле загрузки, оно не участвует в расчёте.'],'table':{'columns':rows[0],'rows':rows[1:]}})
  # CSV copy and SQL initialization must agree except non-assessed timestamp.
  for s in l['sourceData']['sections']:
   if s['title']=='orders.csv' and 'created_at' in s['table']['columns']:
    idx=s['table']['columns'].index('created_at');s['table']['columns'].pop(idx)
    for row in s['table']['rows']:row.pop(idx)
 if l['semester']==7:
  for v in range(1,31):
   row=dict(ds[l['slug']][str(v)]['conditions']['table']['rows'])
   assignments=[]
   for k,value in row.items():
    if k=='variant':continue
    assignments.append(f'SET @{k} = '+(str(value) if re.fullmatch(r'\d+(\.\d+)?',str(value)) else "'"+str(value).replace("'","''")+"'")+';')
   assignments.append('SET @date_to_exclusive = DATE_ADD(@date_to, INTERVAL 1 DAY);')
   section={'title':'parameters.sql','content':['Выполните эти присваивания в той же сессии клиента перед запросами. Дата date_to включена в интервал; date_to_exclusive — следующий день. Символ | разделяет допустимые статусы: он не является оператором IN.','\n'.join(assignments)]}
   ds[l['slug']][str(v)]['sections']=[s for s in ds[l['slug']][str(v)]['sections'] if s['title']!='parameters.sql']+[section]
 for s in l['sourceData']['sections']:
  if s['title'].endswith('.sql') and 'content' in s:s['content']=[re.sub(r':(date_from|date_to_exclusive|order_id|branch_id)',r'@\1',x) for x in s['content']]
for p in (R/'inputs/sql').glob('*.sql'):p.write_text(re.sub(r':(date_from|date_to_exclusive|order_id|branch_id)',r'@\1',p.read_text(encoding='utf-8-sig')),encoding='utf-8')
(R/'src/data/labs.json').write_text(json.dumps({'labs':labs},ensure_ascii=False,indent=2),encoding='utf-8')
(R/'src/data/datasets.json').write_text(json.dumps(ds,ensure_ascii=False,indent=2),encoding='utf-8')
print('SQL tables exported into student CSV sources')
