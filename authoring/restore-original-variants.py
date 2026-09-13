"""Restore the original assignment contract without discarding stand extensions."""
from pathlib import Path
import csv, json, subprocess
R=Path(__file__).resolve().parents[1]
BASE='71901239a970daf8d190d1df0ed0989d47c5ee8c'
def read(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def dump(p,data): (R/p).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def rows(p): return list(csv.DictReader((R/p).read_text(encoding='utf-8-sig').splitlines()))
for path in ['inputs/variants/c4-s8-variants.csv','inputs/incidents/log-windows.csv']:
 (R/path).write_bytes(subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=R))
matrices={s:rows(f'inputs/variants/{c}-s{s}-variants.csv') for s,c in [(6,'c3'),(7,'c4'),(8,'c4')]}
data=read('src/data/datasets.json'); payload=read('src/data/labs.json'); windows=rows('inputs/incidents/log-windows.csv')
for lab in payload['labs']:
 for v in range(1,31):
  data[lab['slug']][str(v)]['conditions']['table']['rows']=list(map(list,matrices[lab['semester']][v-1].items()))
 for section in lab['sourceData']['sections']:
  if section['title']=='log-windows.csv':
   section['table']={'columns':list(windows[0]),'rows':[list(w.values()) for w in windows]}
   section['content']=['Исходные интервалы и параметры сохранены. Если в предоставленном журнале нет записей своего интервала, зафиксируйте недостаточность данных и запросите соответствующий фрагмент; не подменяйте интервал чужим.']
 if lab['semester']==8:
  note='Пороги, метрика и окно наблюдения взяты из исходного варианта без изменения. Пороговые правила в threshold-rules.csv — отдельные исходные правила, а не замена этих условий. Если единицы или направление порога противоречат смыслу метрики, отразите противоречие и предложите обоснованную поправку отдельно от расчёта по исходным условиям.'
  for v in range(1,31): data[lab['slug']][str(v)]['conditions']['content']=[note]
dump('src/data/labs.json',payload);dump('src/data/datasets.json',data)
areas=read('src/data/subject-areas.json'); enterprises=rows('inputs/demo-exam/kod-5-variants.csv')
for area,profile,e in zip(areas['subjectAreas'],areas['profiles'],enterprises):
 v=int(e['variant']); a,b,c=[matrices[s][v-1] for s in [6,7,8]]
 area.update(title=e['enterprise_profile'],description='Профиль предприятия применяется в работе подготовки к демонстрационному экзамену. Для остальных работ используйте их исходные параметры и учебную базу service_ops.',criticalFunction='Условия определяются лабораторной работой')
 profile['title']='Исходные условия'
 profile['characteristics']=[
  {'code':'S6','name':'6 семестр · сервер','value':f"{a['service_name']} · порт {a['port']}",'example':f"Сравнение строк: {a['collation']}; инцидент {a['incident_case']}; журнал {a['log_window']}."},
  {'code':'S7','name':'7 семестр · запросы','value':f"Филиал {b['branch_id']} · сумма от {b['minimum_total']}",'example':f"{b['date_from']} — {b['date_to']}; статусы {b['statuses']}; заказ {b['order_id']}; объём {b['volume_rows']} строк."},
  {'code':'S8','name':'8 семестр · мониторинг','value':f"{c['metric']} · {c['warning_threshold']} / {c['critical_threshold']}",'example':f"Окно {c['evaluation_window']}; приоритет {c['platform_priority']}; инцидент {c['incident_id']}."},
  {'code':'EXAM','name':'Подготовка к демоэкзамену','value':e['enterprise_profile'],'example':f"{e['database_name']}; {e['product_term']}, {e['material_term']}; минимальная сумма {e['minimum_order_total']}."}]
dump('src/data/subject-areas.json',areas)
print('Restored original variant matrices, log windows and 30 enterprise profiles')
