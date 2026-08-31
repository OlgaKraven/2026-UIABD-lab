import { readFile, stat } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const labs = JSON.parse(await readFile(resolve(root, 'content/labs.json'), 'utf8'));
const failures = [];
const expect = (condition, message) => { if (!condition) failures.push(message); };
const grouped = new Map();

expect(labs.length === 22, `Ожидалось 22 работы, найдено ${labs.length}`);
expect(new Set(labs.map((lab) => lab.id)).size === 22, 'ID лабораторных должны быть уникальны');

for (const lab of labs) {
  const key = `${lab.course}-${lab.semester}`;
  grouped.set(key, (grouped.get(key) ?? 0) + 1);
  for (const field of ['id', 'title', 'objective', 'skill', 'scenario', 'artifact', 'reportTemplate', 'teacherGuide']) {
    expect(Boolean(lab[field]), `${lab.id}: не заполнено поле ${field}`);
  }
  expect(lab.durationAcademicHours === 2, `${lab.id}: продолжительность должна быть 2 академических часа`);
  expect(Array.isArray(lab.steps) && lab.steps.length >= 6, `${lab.id}: требуется минимум 6 логических шагов`);
  expect(Array.isArray(lab.evidence) && lab.evidence.length >= 3, `${lab.id}: недостаточно доказательств`);
  expect(!('teacher' in lab), `${lab.id}: закрытые ответы попали в публичные данные`);
  if (lab.course === 4 && lab.semester === 8) {
    expect(lab.demoExam?.code?.includes('09.02.07-5-2027'), `${lab.id}: не указана актуальная связь с КИМ 2027`);
  }
  const paths = [lab.reportTemplate, ...lab.inputFiles];
  for (const path of paths) {
    try { await stat(resolve(root, path.replace(/^\//, ''))); }
    catch { failures.push(`${lab.id}: отсутствует ${path}`); }
  }
}

expect(grouped.get('3-6') === 7, '3 курс, 6 семестр: должно быть 7 работ');
expect(grouped.get('4-7') === 10, '4 курс, 7 семестр: должно быть 10 работ');
expect(grouped.get('4-8') === 5, '4 курс, 8 семестр: должно быть 5 работ');

for (const file of ['inputs/variants/c3-s6-variants.csv', 'inputs/variants/c4-s7-variants.csv', 'inputs/variants/c4-s8-variants.csv', 'inputs/capacity/workload-variants.csv', 'inputs/incidents/log-windows.csv', 'inputs/demo-exam/kod-5-variants.csv', 'inputs/demo-exam/kod-5-api-cases.csv']) {
  const rows = (await readFile(resolve(root, file), 'utf8')).trim().split(/\r?\n/).length - 1;
  expect(rows === 30, `${file}: ожидалось 30 вариантов, найдено ${rows}`);
}
const cases = JSON.parse(await readFile(resolve(root, 'inputs/incidents/connection-cases.json'), 'utf8'));
expect(cases.length === 30, `connection-cases.json: ожидалось 30 кейсов, найдено ${cases.length}`);

const searchable = JSON.stringify(labs).toLocaleLowerCase('ru');
const legacyName = 'mood' + 'le';
expect(!searchable.includes(legacyName), 'В публичном контенте найдено старое название платформы');
expect(!searchable.includes('09.02.07-5-2026'), 'В публичном контенте найден устаревший КОД 2026');
expect(searchable.includes('https://bom.firpo.ru/public/6506'), 'В публичном контенте отсутствует официальная карточка КИМ 2027');

if (failures.length) {
  console.error(failures.map((message) => `- ${message}`).join('\n'));
  process.exit(1);
}
console.log('Content validation passed: 22 labs, 30 variants, KIM 2027, all artifacts linked');
