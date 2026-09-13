from pathlib import Path
import json,csv,subprocess,hashlib
R=Path(__file__).resolve().parents[1]
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
old=json.loads((R/'authoring/original-labs.json').read_text(encoding='utf-8-sig'))
def table(p):
 text=p.read_text(encoding='utf-8-sig');return list(csv.reader(text.splitlines(),delimiter=';' if ';' in text.splitlines()[0] else ','))
variants={s:list(csv.DictReader((R/f'inputs/variants/{c}-s{s}-variants.csv').read_text(encoding='utf-8-sig').splitlines())) for s,c in [(6,'c3'),(7,'c4'),(8,'c4')]}
registry=[]
for i,l in enumerate(old):
 registry.append({k:{'value':v,'status':'взято из первоначального проекта','source':f'content/labs.json[{i}].{k}'} for k,v in {**{k:l[k] for k in ['id','number','title','semester','block','durationAcademicHours']},'topic':l['lectureTopic']['title'],'points':sum(x['points'] for x in l['lms']['rubric'])}.items()})
dump(R/'quality/original-registry.json',registry)
dump(R/'private/lecture-map.json',[{'id':l['id'],'source':l['lectureTopic'],'result':l['artifact']} for l in old])
labs=[];datasets={};method={}
for i,l in enumerate(old):
 key=l['id'];sections=[{'title':'Исходная среда и ограничения','content':l['inputs']+l['constraints']}]
 files=list(dict.fromkeys(l['inputFiles']))
 if l['semester']>=7 and (l['semester']==8 or l['number']<10):
  files=list(dict.fromkeys(['/inputs/sql/service_ops_schema.sql','/inputs/sql/service_ops_seed.sql']+files))
 for path in files:
  if '/variants/' in path:continue
  p=R/path.lstrip('/');txt=p.read_text(encoding='utf-8-sig')
  if p.suffix=='.csv':
   rows=table(p);sections.append({'title':p.name,'content':['Учебные данные. Пустая ячейка означает, что значение не задано. Имена полей сохранены для совместимости со стендом.'],'table':{'columns':rows[0],'rows':rows[1:]}})
  else:sections.append({'title':p.name,'content':[txt]})
 points=sum(x['points'] for x in l['lms']['rubric'])
 new=dict(number=l['number'],slug=key,title=l['title'],block=l['semester']-5,blockTitle=l['block'],semester=l['semester'],topicCode='',topicTitle=l['lectureTopic']['title'],points=points,practicalResult=l['artifact'],situation=l['scenario'],goal=l['objective'],outcomes=[l['skill']],sourceData={'intro':'Версия UIABD-lab-2026.09.13-1. Данные синтетические. Выполняйте SQL только в отдельной учебной базе своего варианта. Сохранённые SQL и конфигурации находятся в папке «Стенд» архива. CSV находятся в папке «Данные».','sections':sections},tools=[l['platform'],'Редактор SQL и текстовых файлов; Word или совместимый редактор DOCX.'],theoryCards=[{'label':f'Правило {j+1}','title':x.split('.')[0],'text':x} for j,x in enumerate(l['reminder']['points'])],task=l['steps'],stages=[],deliverables=[l['artifact']],evidence=l['evidence'],selfCheck=l['checklist'],wordRequirements=l['evidence']+['Укажите вариант, команды и фактические результаты. Удалите серые подсказки. Не включайте секреты.'],professionalChoice=l['reminder']['typicalError'],lmsSteps=[l['lms']['submission'],'Передайте файл в задание LMS, указанное преподавателем. На проверке объясните собственные команды и результаты; допускается письменное объяснение.'],reportFile=f'{key}.docx',recommendedFileName=f'{key}_Вариант_Фамилия_Группа.docx',rubric=l['lms']['rubric'],standFiles=[p.lstrip('/') for p in files if '/variants/' not in p and not p.endswith('.csv')])
 labs.append(new)
 method[key]={'sequence':{'previous': 'Используйте отдельный учебный экземпляр MySQL 8.4. '+('Предыдущая работа не нужна.' if i==0 else 'При необходимости восстановите исходное состояние по схеме и данным в комплекте. Результат текущей работы этим не заменяется.'),'next':'Сохраните '+l['artifact'].lower()+'. Команды и параметры нужны для воспроизведения проверки.'},'example':{'title':'Учебный пример проверки','source':l['reminder']['example'],'method':['Отделите ожидаемое состояние от фактического.','Получите независимое подтверждение указанного признака.'],'result':l['reminder']['successCriterion'],'boundary':'Пример показывает форму проверки. Фактические значения получите в своей учебной среде.'},'steps':[{'data':'; '.join(l['inputs'][:2]),'result':l['evidence'][min(j,len(l['evidence'])-1)],'check':l['reminder']['successCriterion']} for j in range(len(l['steps']))]}
 datasets[key]={}
 for v in range(1,31):
  row=variants[l['semester']][v-1]
  datasets[key][str(v)]={'conditions':{'title':'Параметры варианта','table':{'columns':['Параметр','Значение'],'rows':[[k,val] for k,val in row.items()]}},'sections':[]}
dump(R/'src/data/labs.json',{'labs':labs})
dump(R/'src/data/datasets.json',datasets)
(R/'src/data/methodology.ts').write_text('export interface StepGuide {data:string;result:string;check:string}\nexport const labMethodology:Record<string,{sequence:{previous:string;next:string};example:{title:string;source:string;method:string[];result:string;boundary:string};steps:StepGuide[]} = '+json.dumps(method,ensure_ascii=False,indent=2),encoding='utf-8')
dump(R/'src/data/subject-areas.json',{'profiles':[{'id':v,'title':'Учебный экземпляр','variantRange':f'V{v:02}','characteristics':[{'code':'DB','name':'База данных','value':f'service_ops_{v:02}','example':'Изолированная база своего варианта; параметры конкретной работы приведены ниже.'}]} for v in range(1,31)],'subjectAreas':[{'id':v,'code':f'V{v:02}','title':f'Сервисные операции · вариант {v:02}','systemCode':f'service_ops_{v:02}','description':'Учебная система заказов, материалов и обслуживания.','criticalFunction':'Целостность и доступность базы','assets':['Заказы','Материалы'],'profileId':v,'pack':''} for v in range(1,31)]})
(R/'src/config.ts').write_text("export const courseConfig="+json.dumps(dict(code='МДК.07.01',discipline='Управление и автоматизация баз данных',title='Лабораторный практикум',heroTitle='Управляйте',heroAccent='базами данных',slogan='Настройте сервер, проверьте запросы и автоматизацию, исследуйте показатели и восстановление базы.',materialsUrl='',semesters=[6,7,8],lmsUrl='',logo='brand/synergy-logo.png',mascot='brand/okfks-rhino.webp',blocksTitle='От настройки сервера к восстановлению',blocksDescription='6 семестр — администрирование. 7 семестр — запросы и автоматизация. 8 семестр — мониторинг и восстановление.',demo=False),ensure_ascii=False),encoding='utf-8')
dump(R/'quality/progress.json',{'phase':'migration-in-progress','labs':22,'variants':30,'verified':False,'next':'Subject-specific enrichment, stands, DOCX, browser archives'})
print('Migrated',len(labs),'labs; protected points:',sum(l['points'] for l in labs))
