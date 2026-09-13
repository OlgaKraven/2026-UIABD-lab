"""Deterministic additions to the retained course and stand, version 2026.09.13-1."""
from pathlib import Path
import json,csv,io,re,datetime,shutil
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def dump(p,x):(R/p).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
labs=read('src/data/labs.json')['labs'];data=read('src/data/datasets.json')
p=R/'src/data/methodology.ts';method=json.loads(p.read_text(encoding='utf-8-sig').split(' = ',1)[1])
# Each explanation uses a separate miniature case, never a solved assessed record.
examples=[
('Порт экземпляра','У учебного экземпляра X порт 3407, клиент отправляет запрос на 3306.','SELECT @@port возвращает 3407. В клиенте задайте 3407 и повторите подключение.','Ответ сервера и настройка клиента совпадают: 3407.'),
('Проверка по слоям','Служба X работает, TCP-проверка успешна, вход пользователя отклонён.','Отдельно проверьте службу, порт и SQL-вход. Первые два успеха не доказывают право входа.','Доступность процесса подтверждена; право входа требует отдельной проверки.'),
('Ссылочная целостность','Таблица teams содержит team_id=90. В tasks.team_id требуется ссылка на teams.','Создайте первичный ключ teams, затем внешний ключ tasks. Попытайтесь добавить задачу с team_id=91.','Несуществующая команда отклоняется внешним ключом; значение 90 допустимо.'),
('Импорт через промежуточную таблицу','Две учебные строки X1 и X2 содержат quantity=3 и quantity=-2. Допустимы положительные количества.','Сохраните обе строки как текст в staging; преобразуйте число после проверки формата. Отклонённую строку не удаляйте.','X1 проходит правило количества; X2 остаётся в реестре ошибок.'),
('Минимальные права','Пользователь report_x должен читать таблицу teams, но не менять её.','Войдите именно как report_x. Проверьте SELECT и UPDATE отдельно.','SELECT разрешён; UPDATE отклонён. Проверка под администратором не доказывает права report_x.'),
('Локализация отказа','Клиент получает отказ TCP; служба X остановлена.','Проверьте состояние процесса до изменения паролей. После разрешённого запуска повторите TCP и SQL-проверку.','Нужно подтвердить обе проверки после изменения, а не только исчезновение первой ошибки.'),
('Порядок событий','В журнале X: 08:02 отказ записи, 08:03 остановка, 08:05 успешный запуск.','Упорядочьте записи с одним часовым поясом. Отделите событие от предположения о его причине.','Остановка следует за отказом записи; причина отказа ещё требует проверки диска и прав.'),
('Полуоткрытый интервал','Нужны события июля; столбец happened_at содержит дату и время.','WHERE happened_at >= \'2026-07-01\' AND happened_at < \'2026-08-01\'. Проверьте момент ровно на каждой границе.','Начало июля включено, начало августа исключено; последние секунды июля не потеряны.'),
('Кардинальность соединения','У задачи X есть две строки затрат по 4 и 6 единиц и три комментария.','Соединение обеих детализаций даёт 2×3=6 строк. До соединения агрегируйте затраты по задаче.','Сумма затрат 10; сумма 30 после соединения означала бы размножение строк.'),
('Агрегирование с пустыми значениями','В группе X измерения: 2, NULL, 4.','COUNT(*) считает строки, COUNT(value) — заданные значения; AVG пропускает NULL.','COUNT(*)=3, COUNT(value)=2, AVG(value)=3. Не заменяйте отсутствие измерения нулём без правила.'),
('Две независимые суммы','У учебной операции услуги стоят 2×50, материалы — 3×8.','Посчитайте каждую составляющую независимо, затем сложите агрегаты одного заказа.','Услуги 100, материалы 24, итог 124. Единицы и округление задаются правилом расчёта.'),
('Граница расчёта','Для учебной услуги цена 12.50, количество 0; договор запрещает нулевое количество.','Проверьте отдельно арифметику и допустимость входа. Нулевой итог не означает допустимость записи.','Вход отклоняется по правилу количества, даже если умножение даёт 0.'),
('Атомарность учётной операции','На складе X остаток 8, запрос на расход 9.','Проверьте правило остатка и откат всех изменений при ошибке. Повтор операции с тем же reference_no проверяйте отдельно.','Неуспешный расход не меняет остаток и не оставляет частичную запись движения.'),
('Изменение состояния','У объекта X статус NEW. Выполнены NEW→NEW и NEW→DONE.','Сравните OLD.status и NEW.status. Проверьте число записей аудита после каждого действия и после ROLLBACK.','Первое действие не является сменой статуса; второе является. Откат должен отменять связанный аудит.'),
('Измерение производительности','Три прогона запроса X: 12, 13 и 35 мс.','Укажите одинаковые данные и условия. Отдельно отметьте холодный кеш и сравните несколько прогонов.','Медиана 13 мс; один медленный прогон не доказывает устойчивую регрессию.'),
('Цена индекса','Запрос X фильтрует team_id и сортирует happened_at.','Проверьте составной индекс на том же наборе и плане. Сравните чтение и стоимость записи, затем проверьте другой фильтр.','Индекс принимается по измерениям; его наличие само по себе не доказывает ускорение.'),
('Запас ёмкости','Учебная база 20 GiB растёт на 2 GiB в месяц; горизонт 6 месяцев, запас 25%.','Сначала 20+2×6=32 GiB, затем 32×1.25. Резервные копии учитывайте отдельно по принятой формуле.','Для основных данных требуется 40 GiB; это ещё не вся дисковая ёмкость сервера.'),
('Проверка цепочки сбора','Exporter X отвечает HTTP, но MySQL-метрика отсутствует.','Проверьте endpoint, цель сбора и связь exporter с БД отдельно. Успех HTTP не равен успешному запросу к БД.','Нужны доступная цель и предметная метрика с актуальной меткой времени.'),
('Счётчик и скорость','Счётчик операций X вырос со 100 до 160 за 30 секунд.','Разность делите на интервал: 60/30. При сбросе счётчика используйте обработку counter reset.','Средняя скорость 2 операции/с. Значение 160 — накопленное число, а не скорость.'),
('Направление порога','Свободное место X падает с 30% до 12%; критический порог 15%.','Для свободного места условие value < 15. Отдельно определите удержание условия и поведение при отсутствии данных.','12% ниже критического порога; отсутствие данных нельзя автоматически считать нормой.'),
('Восстановление и проверка','В копии X ожидается 3 записи и сумма 75. После восстановления получено 3 записи и сумма 60.','Проверьте структуру, число строк, контрольную сумму и прикладную операцию отдельно.','Совпадения числа строк недостаточно: восстановленные значения расходятся.'),
('Сравнение на одном случае','Две платформы возвращают одинаковый итог X, но по-разному задают автоинкремент.','Примените один набор и ожидаемый результат, зафиксируйте различия синтаксиса отдельно от функционального результата.','Совместимость запроса и соответствие результата — разные критерии выбора.')]
for i,l in enumerate(labs):
 m=method[l['slug']];title,source,ex,result=examples[i]
 m['example']={'title':title,'source':source,'method':[ex],'result':result,'boundary':'Объекты X используются только в примере и не входят в оцениваемые данные. Выполните аналогичную проверку на данных своего варианта.'}
 l['theoryCards'].insert(0,{'label':'Перед выполнением','title':title,'text':source+' '+ex+' '+result})
 # Preserve original action wording; attach the evidence in the same order as the action.
 for j,(step,g) in enumerate(zip(l['task'],m['steps'])):
  g['data']='Параметры варианта и '+', '.join(s['title'] for s in l['sourceData']['sections'][1:4])+'. Для действий с сервером используйте его фактическое состояние.'
  g['result']=f'Результат действия «{step.rstrip(".")}»: команда или расчёт, полученный вывод и его связь с результатом «{l["practicalResult"]}».'
  g['check']='Запись позволяет повторить именно это действие; параметры совпадают с вариантом. '+l['evidence'][min(j,len(l['evidence'])-1)]
 l['professionalChoice']='Выберите способ проверки, который подтверждает результат: '+l['practicalResult'].lower()+'. Объясните ограничения выбранного доказательства.'
 if i>0:m['sequence']['previous']='Используйте '+labs[i-1]['practicalResult'].lower()+f' из ЛР {labs[i-1]["number"]} семестра {labs[i-1]["semester"]} только в части параметров среды и выполненных проверок. Исходные файлы этой работы позволяют восстановить учебное состояние с помощью преподавателя.'
 if i<len(labs)-1:m['sequence']['next']=f'Сохраните {l["practicalResult"].lower()}. В ЛР {labs[i+1]["number"]} семестра {labs[i+1]["semester"]} пригодятся параметры среды и результаты проверки.'
# Correct dimensional errors in the inherited monitoring variant matrix.
vp=R/'inputs/variants/c4-s8-variants.csv';rows=list(csv.DictReader(vp.read_text(encoding='utf-8-sig').splitlines()))
for r in rows:
 v=int(r['variant']);metric=r['metric'];base={'connections_used_pct':(60,80,'above','%'),'p95_query_seconds':(.8,1.5,'above','s'),'disk_free_pct':(25,15,'below','%'),'error_rate_per_min':(3,8,'above','1/min')}[metric]
 r.update(warning_threshold=str(base[0]),critical_threshold=str(base[1]),direction=base[2],unit=base[3])
with vp.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=';');w.writeheader();w.writerows(rows)
# Repair existing volume loader: MySQL puts WITH after INSERT INTO, and default recursive depth is too small.
volume=R/'inputs/sql/generate_volume.sql'
volume.write_text("""-- MySQL 8.4. Только учебная база; @volume_rows задайте по варианту.
SET @volume_rows = COALESCE(@volume_rows, 25000);
INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status)
WITH digits AS (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9),
seq AS (SELECT 1+a.n+10*b.n+100*c.n+1000*d.n+10000*e.n n FROM digits a CROSS JOIN digits b CROSS JOIN digits c CROSS JOIN digits d CROSS JOIN digits e)
SELECT 100000+n, CONCAT('LOAD-',LPAD(n,6,'0')),1+MOD(n,3),1+MOD(n,9),DATE_ADD('2025-01-01',INTERVAL MOD(n,730) DAY),ELT(1+MOD(n,4),'NEW','IN_PROGRESS','DONE','CANCELLED')
FROM seq WHERE n<=@volume_rows AND NOT EXISTS(SELECT 1 FROM orders o WHERE o.order_id=100000+n);
INSERT INTO order_items(order_id,line_no,service_id,quantity)
SELECT order_id,1,1+MOD(order_id,4),1+MOD(order_id,3) FROM orders o
WHERE order_id>=100001 AND order_id<=100000+@volume_rows AND NOT EXISTS(SELECT 1 FROM order_items i WHERE i.order_id=o.order_id AND i.line_no=1);
""",encoding='utf-8')
# Expand retained IDs 1001..1012 to the 1030 referenced by the existing 30 variants.
seed=R/'inputs/sql/service_ops_seed.sql';txt=seed.read_text(encoding='utf-8')
if '-- Extended assessed orders' not in txt:
 txt+='\n-- Extended assessed orders 1013..1030; original records retained.\n'
 for v in range(13,31):txt+=f"INSERT INTO orders(order_id,external_order_no,branch_id,customer_id,order_date,status) VALUES({1000+v},'SO-{1000+v}',{1+(v-1)%3},{1+(v-1)%9},'2026-{2+(v-1)%5:02}-15','DONE');\nINSERT INTO order_items VALUES({1000+v},1,{1+(v-1)%4},{1+v%3});\n"
 seed.write_text(txt,encoding='utf-8')
# Assessment cases are structured CSV and expand by complexity; measured results remain blank.
for i,l in enumerate(labs):
 key=l['slug'];level=1 if i<2 else 2 if i<7 else 3 if i<17 else 4
 count={1:8,2:16,3:24,4:32}[level]
 for v in range(1,31):
  ds=data[key][str(v)]
  if l['semester']==8:ds['conditions']['table']['rows']=[[k,x] for k,x in rows[v-1].items()]
  records=[]
  for n in range(count):
   # This is an explicit experiment plan, not fabricated observations.
   evidence=l['evidence'][n%len(l['evidence'])]
   cases=['исходное состояние','граничное допустимое условие','недопустимое условие','повтор действия']
   records.append([f'{key}-V{v:02}-T{n+1:02}',n//4+1,cases[(n+v-1)%4],evidence,''])
  # Include only for tests where repeated experimental cases are meaningful.
  if key in ['C4_S7_LR05','C4_S7_LR06','C4_S7_LR07']:
   ds['sections']=[{'title':'План самостоятельных проверок','content':['Это план эксперимента, не готовые измерения. Укажите конкретный вход, ожидаемый результат до запуска, затем фактический вывод. Для каждой записи выполните соответствующую проверку.'],'table':{'columns':['test_id','Группа','Условие','Доказательство','Фактический результат'],'rows':records}}]
  if l['semester']==8 and l['number'] in [1,2,3,4]:
   metrics=[]
   for n in range(32):
    t=datetime.datetime(2026,8,20,10,0,tzinfo=datetime.timezone.utc)+datetime.timedelta(minutes=5*n)
    phase=(n+v)%16
    metrics.append([f'V{v:02}-M{n+1:02}',t.isoformat().replace('+00:00','Z'),40+phase*3,round(.25+phase*.11,2),max(5,38-phase*2),phase//2,'missing' if n==(v%25) else 'ok'])
   ds['sections']=[{'title':'Новый период наблюдения','content':['Учебный ряд для самостоятельной проверки. Время UTC; шаг 5 минут. connections_used_pct и disk_free_pct — проценты; p95_query_seconds — секунды; error_rate_per_min — ошибок/мин. Строка missing означает отсутствие измерения: её числа не используйте. Не выдавайте этот ряд за измерение своей системы. Сопоставьте его с исходным периодом и объясните изменение вывода.'],'table':{'columns':['sample_id','timestamp','connections_used_pct','p95_query_seconds','disk_free_pct','error_rate_per_min','sample_state'],'rows':metrics}}]
 # Refresh all original input text, remove closed answer fields in diagnostic source.
 for section in l['sourceData']['sections']:
  matches=list((R/'inputs').rglob(section['title'])) if '.' in section['title'] else []
  if len(matches)==1 and 'content' in section and matches[0].suffix!='.csv':section['content']=[matches[0].read_text(encoding='utf-8-sig')]
  if section['title']=='connection-cases.json':
   cases=json.loads(section['content'][0]);section['content']=[json.dumps([{k:v for k,v in c.items() if k not in ['fault','allowedChange']} for c in cases],ensure_ascii=False,indent=2)]
dump('src/data/labs.json',{'labs':labs});dump('src/data/datasets.json',data)
p.write_text('export interface StepGuide {data:string;result:string;check:string}\nexport const labMethodology:Record<string,{sequence:{previous:string;next:string};example:{title:string;source:string;method:string[];result:string;boundary:string};steps:StepGuide[]}> = '+json.dumps(method,ensure_ascii=False,indent=2),encoding='utf-8')
dump('authoring/methodology.json',method)
dump('quality/content-changes.json',{'preserved':'22 identities, 220 points, 30 variants and all original stand components','changes':['MySQL volume loader syntax and repeatability','Orders 1013–1030 added to match existing variants','Monitoring thresholds corrected by units and direction','Independent miniature examples in 22 labs','New monitoring period with missing-data case'], 'pending':'Full subject and artifact verification'})
print('Enriched 22 labs')
