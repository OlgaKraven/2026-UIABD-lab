from pathlib import Path
import json,csv,copy
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'src/data/datasets.json').read_text(encoding='utf-8'))
original=list(csv.reader((R/'inputs/csv/orders_import.csv').read_text(encoding='utf-8-sig').splitlines(),delimiter=';'))
keys=[]
for v in range(1,31):
 rows=copy.deepcopy(original[1:]);defects=[]
 for n in range(24):
  row=[f'EXT-V{v:02}-{n+1:02}',str(1+(v+n)%3),str(1+(v*2+n)%9),f'2026-{2+(n%5):02}-{1+n%27:02}',str(1+n%12),['NEW','IN_PROGRESS','DONE','CANCELLED'][(v+n)%4]]
  case=(v+n)%8
  if case==0:row[1]='99';defects.append({'row':row[0],'reason':'unknown branch'})
  elif case==2:row[4]='0';defects.append({'row':row[0],'reason':'quantity out of range'})
  elif case==4:row[3]='2026-02-30';defects.append({'row':row[0],'reason':'invalid calendar date'})
  elif case==6:row[5]='PENDING';defects.append({'row':row[0],'reason':'unknown status'})
  rows.append(row)
 data['C3_S6_LR04'][str(v)]['sections']=[{'title':'orders_import.csv','content':['Сохранены исходные записи EXT-260x и добавлена новая партия EXT-Vxx. Проверьте обе партии по одним правилам импорта. Не меняйте исходный CSV: ошибки фиксируйте в промежуточной таблице и реестре отклонений. Количество рабочих записей: '+str(len(rows))+'.'],'table':{'columns':original[0],'rows':rows}}]
 keys.append({'variant':v,'new_batch_defects':defects,'original_rows':'Retained original defects; see original teacher guide'})
(R/'src/data/datasets.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'private/import-keys.json').write_text(json.dumps(keys,ensure_ascii=False,indent=2),encoding='utf-8')
print('30 import batches extended without replacing original rows')
