from pathlib import Path
import json,copy,hashlib
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
R=Path(__file__).resolve().parents[1]
REF=R.parent/'lab-template/public/reports/LAB03_template.docx'
labs=json.loads((R/'src/data/labs.json').read_text(encoding='utf-8-sig'))['labs']
method=json.loads((R/'authoring/methodology.json').read_text(encoding='utf-8'))
def fmt(p,bold=False,hint=False):
 p.paragraph_format.space_after=Pt(6)
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12);r.font.bold=bold;r.font.italic=hint;r.font.color.rgb=RGBColor.from_string('666666' if hint else '000000')
def para(d,text,bold=False,hint=False):
 p=d.add_paragraph(text,style='Heading 2' if bold else 'Normal');fmt(p,bold,hint);return p
def table(d,heads,rows=2):
 t=d.add_table(rows=1,cols=len(heads));t.autofit=False
 for c,h in zip(t.rows[0].cells,heads):
  c.text=h;sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E5EEF8');c._tc.get_or_add_tcPr().append(sh)
 hdr=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(hdr)
 for _ in range(rows):t.add_row()
 for row in t.rows:
  for c in row.cells:
   c.width=Cm(16.5/len(heads))
   borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
   c._tc.get_or_add_tcPr().append(borders)
   for p in c.paragraphs:fmt(p,row==t.rows[0])
 return t
def allparas(d):
 yield from d.paragraphs
 for t in d.tables:
  for row in t.rows:
   for c in row.cells:yield from c.paragraphs
for lab in labs:
 d=Document(REF)
 # Retain cover up to its first explicit page break, including logos and identity tables.
 body=d._element.body;cut=None
 for idx,el in enumerate(body):
  if el.xpath('.//w:br[@w:type="page"]'):cut=idx;break
 if cut is None:raise RuntimeError('No cover boundary')
 for el in list(body)[cut+1:]:
  if el.tag!=qn('w:sectPr'):body.remove(el)
 replacements={'Предложение улучшения':lab['title'],'Отчёт по лабораторной работе № 3':f'Отчёт по лабораторной работе № {lab["number"]}','[Курс] · 2 семестр · ЛР03':f'{3 if lab["semester"]==6 else 4} курс · {lab["semester"]} семестр · ЛР{lab["number"]:02}','[Название факультета]':'Информационных технологий','[Код и название специальности]':'09.02.07 Информационные системы и программирование','[Форма обучения]':'Очная','[Название дисциплины]':'МДК.07.01 Управление и автоматизация баз данных','[Город], [Год]':'Москва, 2026'}
 for p in allparas(d):
  text=p.text
  for a,b in replacements.items():text=text.replace(a,b)
  if text!=p.text:p.text=text
  # Preserve the reference cover spacing so the city/year stays on its cover.
  for run in p.runs:run.font.name='Times New Roman';run.font.size=Pt(12)
 for sec in d.sections:sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.left_margin=Cm(3);sec.right_margin=Cm(1.5);sec.top_margin=Cm(2);sec.bottom_margin=Cm(2)
 for style in d.styles:
  if hasattr(style,'font'):style.font.name='Times New Roman';style.font.size=Pt(12);style.font.color.rgb=RGBColor(0,0,0)
 d.add_page_break()
 para(d,lab['title'],True)
 para(d,f'ЛР {lab["number"]} · семестр {lab["semester"]} · максимум {lab["points"]} баллов')
 para(d,'Вариант ____________    Версия данных UIABD-lab-2026.09.13-1')
 para(d,'Цель: '+lab['goal'])
 para(d,'Результат: '+lab['practicalResult'])
 para(d,'Откройте задание HTML и файлы своего варианта. Заполняйте поля по собственным действиям. Таблицы расширяются: добавляйте строки, не переписывайте весь CSV. Серые подсказки удалите перед сдачей.',hint=True)
 # Evidence forms remain specific to the original technical deliverables.
 for n,e in enumerate(lab['evidence']):
  para(d,f'{n+1} {e.rstrip(".")}',True)
  para(d,'Запишите параметры, команду и фактический результат с объяснением.',hint=True)
  if any(word in e.lower() for word in ['таблиц','матриц','сравн','план','границ','параметр','протокол']):
   heads=['Параметр или случай','Ожидалось','Получено и объяснение'] if lab['semester']!=8 else ['Показатель или событие','Наблюдение','Основание вывода']
   table(d,heads)
  else:para(d,'[Впишите результат и команду либо расчёт.]',hint=True)
 if any('схем' in x.lower() or 'скриншот' in x.lower() for x in lab['evidence']):
  para(d,'Иллюстрация результата',True)
  table(d,['Место для схемы или снимка экрана'],2)
  para(d,'Рисунок № — Название').alignment=1
  para(d,'Впишите номер и название рисунка самостоятельно.',hint=True)
 if lab['slug'] in ['C4_S7_LR05','C4_S7_LR06','C4_S7_LR07'] or (lab['semester']==8 and lab['number']<5):
  para(d,'Результаты нового набора своего варианта',True)
  para(d,'Запишите итог по каждому ID из нового набора. Добавьте строки либо приложите компактную таблицу обработки в этот документ. Один обычный и один граничный случай объясните подробно.',hint=True)
  table(d,['ID случая','Ожидалось','Получено и объяснение'])
 para(d,'Проверка и ограничения вывода',True)
 para(d,'Опишите независимую проверку результата, граничный случай и условия, при которых вывод потребует пересмотра.',hint=True)
 para(d,'[Ваше объяснение.]',hint=True)
 para(d,'Критерии оценки',True)
 t=table(d,['Результат','Баллы'],0)
 for r in lab['rubric']:
  cells=t.add_row().cells;cells[0].text=r['criterion'];cells[1].text=str(r['points'])
  for c in cells:
   for p in c.paragraphs:fmt(p)
 for row in t.rows[:-1]:
  for cell in row.cells:
   for paragraph in cell.paragraphs:paragraph.paragraph_format.keep_with_next=True
 para(d,'Критерии оцениваются независимо в пределах максимума. Объясните собственные команды и результаты; допускается письменное объяснение. Повтор одного доказательства не даёт дополнительных баллов.')
 # The recommended filename is supplied by the site and HTML; avoid an orphan instruction page in Word.
 for rel in list(d.part.rels.values()):
  if rel.is_external:d.part.drop_rel(rel.rId)
 for p in allparas(d):
  for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12)
 for size in d._element.xpath('//w:rPr/w:sz | //w:rPr/w:szCs'):size.set(qn('w:val'),'24')
 for fonts in d._element.xpath('//w:rPr/w:rFonts'):
  for attr in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+attr),'Times New Roman')
 target=R/'public/reports'/lab['reportFile'];d.save(target)
print('Created 22 editable forms from retained reference')
