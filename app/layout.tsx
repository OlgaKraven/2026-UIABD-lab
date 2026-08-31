import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'МДК.07.01 · Лабораторные работы',
  description: '22 лабораторные работы по управлению и автоматизации баз данных: задания, исходные данные, лекции и DOCX-шаблоны.',
  openGraph: {
    title: 'МДК.07.01 · Лабораторные работы',
    description: 'От запуска MySQL — к диагностике, производительности и мониторингу.',
    images: ['/og.png'],
    type: 'website',
    locale: 'ru_RU',
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="ru"><body>{children}</body></html>;
}
