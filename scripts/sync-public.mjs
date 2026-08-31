import { cp, mkdir, rm } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const copies = [
  ['inputs', 'public/inputs'],
  ['reports/student', 'public/reports/student'],
];

for (const [source, destination] of copies) {
  const from = resolve(root, source);
  const to = resolve(root, destination);
  await rm(to, { recursive: true, force: true });
  await mkdir(to, { recursive: true });
  await cp(from, to, { recursive: true });
}

console.log('Synced student downloads to public/');
