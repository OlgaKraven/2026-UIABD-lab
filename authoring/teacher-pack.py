from pathlib import Path
import json,csv,shutil
R=Path(__file__).resolve().parents[1]
labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs'];old=json.loads((R/'authoring/original-labs.json').read_text(encoding='utf-8-sig'));guides=json.loads((R/'content/teacher-guides.json').read_text(encoding='utf-8-sig'));datasets=json.loads((R/'src/data/datasets.json').read_text(encoding='utf-8'))
times=[75,90,130,150,140,140,150,140,150,150,160,180,200,180,170,170,180,170,180,180,200,210]
for i,l in enumerate(labs):
 source=old[i];g=guides[l['slug']]
 text=f'# {l["slug"]} — {l["title"]}\n\n'+f'Максимум: {l["points"]}. Исходный план: 2 академических часа (90 минут). Авторская оценка обновлённой работы: {times[i]} минут. Это не результат прохождения студентом; при расхождении требуется планирование преподавателя, официальный план не изменён.\n\n'
 text+='## Методическая опора\n\n'+l['goal']+'\n\n'+g['referenceCheck']+'\n\nТипичная ошибка: '+g['focus']+'\n\nДиагностическая гипотеза: '+g['rootCause']+'\n\n'
 text+='## Допустимые решения\n\n'+'\n'.join('- '+x for x in g.get('alternatives',[]))+'\n\n'
 text+='## Помощь\n\n1. Напомните понятие из памятки текущей работы.\n2. Предложите сопоставить наблюдение с условием варианта и независимой проверкой.\n3. Разберите отдельный пример X, не подставляя данные оцениваемой строки.\n\n'
 text+='## Проверка понимания\n\n'+'\n'.join('- '+x for x in g.get('discussion',[])[:3])+'\n- Измените один параметр своего варианта: какой результат изменится и какой останется прежним? Обоснуйте на собственном коде.\n\n'
 text+='## Опорные результаты вариантов\n\nДля SQL-фильтра и стоимости используйте mysql-variant-keys.json, полученный на MySQL 8.4. Для вариантов мониторинга используйте monitoring-keys.json: это классификация мгновенных значений, не замена проверки удержания порога. Для открытых решений оцените соответствие условиям и воспроизводимость доказательства; совпадение текста с образцом не требуется.\n\n'
 text+='## Частичная оценка\n\n'+ '\n'.join(f'- {r["criterion"]}: до {r["points"]}; полный балл при проверяемом результате, половина при верном методе и локальной ошибке, 0 при отсутствии доказательства.' for r in l['rubric'])+'\n\nОдин и тот же результат не оценивается дважды. Если ошибка исходных данных делает вывод недостаточным, принимайте обоснование недостаточности и план проверки.\n'
 (R/'private'/f'{l["slug"]}.md').write_text(text,encoding='utf-8')
keys=[]
for l in labs:
 if l['semester']!=8 or l['number']>4:continue
 for v in range(1,31):
  d=datasets[l['slug']][str(v)];c=dict(d['conditions']['table']['rows']);table=d['sections'][0]['table'];idx=table['columns'].index(c['metric']);warning=float(c['warning_threshold']);critical=float(c['critical_threshold']);direction='below' if c['metric']=='disk_free_pct' else 'above'
  out=[]
  for row in table['rows']:
   value=float(row[idx]);status='no_data' if row[-1]=='missing' else ('critical' if (value>critical if direction=='above' else value<critical) else 'warning' if (value>warning if direction=='above' else value<warning) else 'normal')
   if direction=='below' and warning>=critical and status!='no_data':status='requires_threshold_clarification'
   out.append({'id':row[0],'value':value,'instant_state':status})
  keys.append({'lab':l['slug'],'variant':v,'metric':c['metric'],'warning':warning,'critical':critical,'directionAssumption':direction,'states':out})
(R/'private/monitoring-keys.json').write_text(json.dumps(keys,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(R/'quality/original-registry.json',R/'private/original-registry.json')
(R/'private/planning.json').write_text(json.dumps([{'lab':l['slug'],'minutes':times[i],'sourceAcademicHours':2,'status':'author estimate; novice trial not performed'} for i,l in enumerate(labs)],ensure_ascii=False,indent=2),encoding='utf-8')
print('22 teacher cards and 120 monitoring keys prepared')
