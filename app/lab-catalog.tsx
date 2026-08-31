'use client';

import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Boxes,
  CheckCircle2,
  ClipboardCheck,
  Database,
  Download,
  ExternalLink,
  FileCode2,
  FileText,
  Filter,
  Gauge,
  GraduationCap,
  Lightbulb,
  Route,
  Search,
  ShieldCheck,
  Target,
  TerminalSquare,
} from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';
import labsData from '../content/labs.json';

type RubricItem = { criterion: string; points: number };
type Lab = {
  id: string;
  course: number;
  semester: number;
  block: string;
  competencies: string[];
  number: number;
  title: string;
  lectureTopic: { title: string; url: string };
  objective: string;
  skill: string;
  scenario: string;
  inputs: string[];
  constraints: string[];
  steps: string[];
  reminder: { points: string[]; example: string; typicalError: string; successCriterion: string };
  artifact: string;
  evidence: string[];
  checklist: string[];
  reflection: string[];
  lms: { format: string; recommendedName: string; submission: string; rubric: RubricItem[] };
  reportTemplate: string;
  inputFiles: string[];
  sources: { label: string; url: string }[];
  durationAcademicHours: number;
  platform: string;
  demoExam?: {
    code: string;
    level: string;
    mapsTo: string[];
    evidence: string;
    boundary: string;
  };
};

const labs = labsData as Lab[];
const blocks = [...new Set(labs.map((lab) => lab.block))];
const LMS_URL = 'https://synergy.ru/students';

function assetUrl(path: string) {
  return `./${path.replace(/^\//, '')}`;
}

function getRoute() {
  if (typeof window === 'undefined') return null;
  const match = window.location.hash.match(/^#\/lab\/([^/]+)$/);
  return match ? decodeURIComponent(match[1]) : null;
}

function shortFile(path: string) {
  return decodeURIComponent(path.split('/').at(-1) ?? path);
}

export default function LabCatalog() {
  const [activeLabId, setActiveLabId] = useState<string | null>(null);
  const pageStartRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const syncRoute = () => setActiveLabId(getRoute());
    syncRoute();
    window.addEventListener('hashchange', syncRoute);
    return () => window.removeEventListener('hashchange', syncRoute);
  }, []);

  useEffect(() => {
    const lab = labs.find((item) => item.id === activeLabId);
    document.title = lab ? `${lab.id} · ${lab.title}` : 'МДК.07.01 · Лабораторные работы';
    window.scrollTo({ top: 0, behavior: 'instant' });
    pageStartRef.current?.focus({ preventScroll: true });
  }, [activeLabId]);

  const activeLab = labs.find((lab) => lab.id === activeLabId);
  return activeLab ? <LabPage lab={activeLab} pageStartRef={pageStartRef} /> : <Catalog pageStartRef={pageStartRef} />;
}

function Catalog({ pageStartRef }: { pageStartRef: React.RefObject<HTMLElement | null> }) {
  const [query, setQuery] = useState('');
  const [course, setCourse] = useState('all');
  const [semester, setSemester] = useState('all');
  const [block, setBlock] = useState('all');

  const visible = useMemo(
    () => labs.filter((lab) => {
      const haystack = `${lab.id} ${lab.title} ${lab.block} ${lab.artifact} ${lab.objective}`.toLocaleLowerCase('ru');
      return (course === 'all' || String(lab.course) === course)
        && (semester === 'all' || String(lab.semester) === semester)
        && (block === 'all' || lab.block === block)
        && haystack.includes(query.trim().toLocaleLowerCase('ru'));
    }),
    [block, course, query, semester],
  );

  const resetFilters = () => {
    setQuery('');
    setCourse('all');
    setSemester('all');
    setBlock('all');
  };

  return <>
    <a className="skip-link" href="#catalog">К каталогу</a>
    <header className="hero" ref={pageStartRef} tabIndex={-1}>
      <div className="hero__copy">
        <div className="course-brand" aria-label="Московский университет «Синергия»">
          <span className="course-brand__mark">S</span>
          <span><b>Университет</b><strong>СИНЕРГИЯ</strong></span>
        </div>
        <p className="eyebrow">МДК.07.01 · 2026–2027</p>
        <h1>Управление и автоматизация баз данных</h1>
        <p className="lead">От запуска MySQL — к доказательной диагностике, производительности и наблюдению за сервером.</p>
        <div className="metrics" aria-label="Структура курса"><span><b>22</b> работы</span><span><b>3</b> семестра</span><span><b>30</b> вариантов</span><span><b>1</b> DOCX на сдачу</span></div>
      </div>
      <div className="hero-console" aria-label="Маршрут курса">
        <div className="hero-console__top"><Database aria-hidden="true" /><span>service_ops</span><i>READY</i></div>
        <code><em>01</em> install · configure</code><code><em>02</em> query · automate</code><code><em>03</em> measure · recover</code>
        <div className="hero-console__pulse"><span /><span /><span /><span /><span /><span /><span /></div>
      </div>
    </header>
    <main id="catalog" className="catalog">
      <section className="intro" aria-labelledby="catalog-title">
        <div><p className="eyebrow">КАТАЛОГ</p><h2 id="catalog-title">Выберите лабораторную</h2></div>
        <p><BookOpen aria-hidden="true" /> Каждая карточка ведёт к заданию, лекции, исходным данным и редактируемому шаблону отчёта.</p>
      </section>
      <section className="filters" aria-label="Фильтры каталога">
        <label className="search"><Search aria-hidden="true" /><span className="sr-only">Поиск</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ID, название или результат" /></label>
        <div className="filter-row">
          <Filter aria-hidden="true" />
          <label><span>Курс</span><select value={course} onChange={(event) => setCourse(event.target.value)}><option value="all">Все</option><option value="3">3 курс</option><option value="4">4 курс</option></select></label>
          <label><span>Семестр</span><select value={semester} onChange={(event) => setSemester(event.target.value)}><option value="all">Все</option><option value="6">6</option><option value="7">7</option><option value="8">8</option></select></label>
          <label className="section-filter"><span>Учебный блок</span><select value={block} onChange={(event) => setBlock(event.target.value)}><option value="all">Все блоки</option>{blocks.map((item) => <option key={item}>{item}</option>)}</select></label>
        </div>
      </section>
      <div className="catalog-status" aria-live="polite"><b>{visible.length}</b> из 22 работ</div>
      {visible.length ? <section className="grid" aria-label="Лабораторные работы">{visible.map((lab) => <article className="card" key={lab.id}>
        <div className="card__meta"><span>{lab.id}</span><span>{lab.course} курс · {lab.semester} семестр</span></div>
        <p className="card__section">{lab.platform}</p><h3>{lab.title}</h3>
        <div className="result"><span>Результат</span><p>{lab.artifact}</p></div>
        <div className="card__actions"><a className="primary-action" href={`#/lab/${lab.id}`}>Открыть работу <ArrowRight aria-hidden="true" /></a><a className="icon-button" href={assetUrl(lab.reportTemplate)} download aria-label={`Скачать шаблон ${lab.id}`}><Download aria-hidden="true" /></a></div>
      </article>)}</section> : <div className="empty"><p>По этим условиям работ не найдено.</p><button type="button" onClick={resetFilters}>Сбросить фильтры</button></div>}
    </main>
    <SiteFooter />
  </>;
}

function LabPage({ lab, pageStartRef }: { lab: Lab; pageStartRef: React.RefObject<HTMLElement | null> }) {
  return <>
    <a className="skip-link" href="#lab-content">К заданию</a>
    <header className="lab-header" ref={pageStartRef} tabIndex={-1}>
      <nav className="breadcrumbs" aria-label="Навигация"><a href="#catalog"><ArrowLeft aria-hidden="true" /> Каталог</a><span>/</span><span>{lab.id}</span></nav>
      <div className="lab-header__grid"><div><p className="eyebrow">{lab.course} КУРС · {lab.semester} СЕМЕСТР · ЛР {String(lab.number).padStart(2, '0')}</p><h1>{lab.title}</h1><p className="lab-result"><span>Результат работы</span>{lab.artifact}</p></div>
        <div className="quick-actions" aria-label="Материалы работы"><a className="primary-action" href={assetUrl(lab.reportTemplate)} download><Download aria-hidden="true" />Скачать DOCX</a><a href="#source-files"><FileCode2 aria-hidden="true" />Исходные данные<ArrowRight aria-hidden="true" /></a><a href={LMS_URL} target="_blank" rel="noreferrer"><GraduationCap aria-hidden="true" />Открыть LMS<ExternalLink aria-hidden="true" /></a></div></div>
    </header>
    <main id="lab-content" className="lab-layout">
      <section className="lab-main">
        <ContentBlock icon={<Database />} kicker="01 · Контекст" title="Рабочая ситуация"><p>{lab.scenario}</p><p><b>Вариант:</b> 01–30, по строке студента в матрице {lab.course} курса, {lab.semester} семестра.</p><p className="competencies">{lab.competencies.join(' · ')}</p></ContentBlock>
        <ContentBlock icon={<Target />} kicker="02 · Результат обучения" title="Цель и формируемое умение"><p><b>Цель.</b> {lab.objective}</p><p><b>Умение.</b> {lab.skill}</p></ContentBlock>
        <ContentBlock icon={<Boxes />} kicker="03 · Стартовый пакет" title="Исходные данные"><BulletList items={lab.inputs} /><div id="source-files" className="file-list">{lab.inputFiles.map((file) => <a key={file} href={assetUrl(file)} download><FileText aria-hidden="true" /><span>{shortFile(file)}</span><Download aria-hidden="true" /></a>)}</div></ContentBlock>
        <ContentBlock icon={<ShieldCheck />} kicker="04 · Границы" title="Условия выполнения"><BulletList items={lab.constraints} /><p className="note">Продолжительность работы: {lab.durationAcademicHours} академических часа. Разбиение по минутам не задаётся.</p></ContentBlock>
        <ContentBlock icon={<Lightbulb />} kicker="05 · Перед началом" title="Мини-памятка"><BulletList items={lab.reminder.points} numbered /><aside className="decision-callout"><b>Признак готовности</b><p>{lab.reminder.successCriterion}</p></aside></ContentBlock>
        <ContentBlock icon={<Route />} kicker="06 · Действия" title="Маршрут выполнения"><BulletList items={lab.steps} numbered /></ContentBlock>
        <ContentBlock icon={<TerminalSquare />} kicker="07 · Ориентир" title="Мини-пример"><p>{lab.reminder.example}</p><p className="error-note"><b>Типичная ошибка.</b> {lab.reminder.typicalError}</p></ContentBlock>
        <ContentBlock icon={<Gauge />} kicker="08 · Доказательства" title="Что подтвердить"><BulletList items={lab.evidence} /></ContentBlock>
        {lab.demoExam && <ContentBlock icon={<GraduationCap />} kicker="09 · Демонстрационный экзамен" title="Связь с КИМ 2027"><div className="demo-exam"><p className="demo-exam__code">{lab.demoExam.code}</p><p><b>Уровень связи:</b> {lab.demoExam.level}</p><BulletList items={lab.demoExam.mapsTo} /><p><b>Доказательство:</b> {lab.demoExam.evidence}</p><p className="note"><b>Граница:</b> {lab.demoExam.boundary}</p><a className="text-link" href="https://bom.firpo.ru/Public/6506" target="_blank" rel="noreferrer">Официальная карточка КИМ <ExternalLink aria-hidden="true" /></a></div></ContentBlock>}
        <ContentBlock icon={<ClipboardCheck />} kicker={`${lab.demoExam ? '10' : '09'} · Отчёт и LMS`} title="Что сдаётся"><p><b>{lab.lms.submission}</b></p><p>Рекомендуемое имя: <code>{lab.lms.recommendedName}</code></p><div className="rubric">{lab.lms.rubric.map((item) => <div key={item.criterion}><span>{item.criterion}</span><b>{item.points}</b></div>)}</div><a className="inline-link" href={assetUrl(lab.reportTemplate)} download>Скачать редактируемый DOCX <Download aria-hidden="true" /></a><a className="text-link" href={LMS_URL} target="_blank" rel="noreferrer">Перейти к информации о Synergy LMS <ExternalLink aria-hidden="true" /></a></ContentBlock>
        <ContentBlock icon={<CheckCircle2 />} kicker={`${lab.demoExam ? '11' : '10'} · Перед отправкой`} title="Самопроверка"><ul className="checklist">{lab.checklist.map((item) => <li key={item}><CheckCircle2 aria-hidden="true" />{item}</li>)}</ul><div className="reflection">{lab.reflection.map((question) => <p key={question}>{question}</p>)}</div></ContentBlock>
        <ContentBlock icon={<BookOpen />} kicker={`${lab.demoExam ? '12' : '11'} · Теория`} title="Лекция и источники"><div className="lecture-list"><a href={lab.lectureTopic.url} target="_blank" rel="noreferrer"><span>01</span><b>{lab.lectureTopic.title}</b><ExternalLink aria-hidden="true" /></a>{lab.sources.map((source, index) => <a key={source.url} href={source.url} target="_blank" rel="noreferrer"><span>{String(index + 2).padStart(2, '0')}</span><b>{source.label}</b><ExternalLink aria-hidden="true" /></a>)}</div></ContentBlock>
      </section>
      <aside className="lab-sidebar" aria-label="Краткая карточка работы"><div className="sticky-card"><p className="eyebrow">КАРТОЧКА РАБОТЫ</p><dl><div><dt>ID</dt><dd>{lab.id}</dd></div><div><dt>Платформа</dt><dd>{lab.platform}</dd></div><div><dt>Артефакт</dt><dd>{lab.artifact}</dd></div><div><dt>Учебный блок</dt><dd>{lab.block}</dd></div></dl><a className="primary-action" href={assetUrl(lab.reportTemplate)} download><Download aria-hidden="true" />Скачать шаблон</a><a className="back-link" href="#catalog"><ArrowLeft aria-hidden="true" />Ко всем работам</a></div></aside>
    </main>
    <SiteFooter />
  </>;
}

function ContentBlock({ icon, kicker, title, children }: { icon: React.ReactNode; kicker: string; title: string; children: React.ReactNode }) {
  return <section className="content-block"><div className="content-block__head"><span className="block-icon" aria-hidden="true">{icon}</span><div><p>{kicker}</p><h2>{title}</h2></div></div><div className="content-block__body">{children}</div></section>;
}

function BulletList({ items, numbered = false }: { items: string[]; numbered?: boolean }) {
  const Tag = numbered ? 'ol' : 'ul';
  return <Tag className={numbered ? 'numbered-list' : 'bullet-list'}>{items.map((item) => <li key={item}>{item}</li>)}</Tag>;
}

function SiteFooter() {
  return <footer className="site-footer"><div><span className="footer-mark">S</span><p><b>МДК.07.01</b><br />Управление и автоматизация баз данных</p></div><a href="#catalog">Каталог 22 лабораторных</a></footer>;
}
