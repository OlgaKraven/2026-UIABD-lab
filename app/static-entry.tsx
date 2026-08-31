import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import LabCatalog from './lab-catalog';
import './globals.css';

const root = document.querySelector('#root');

if (!root) throw new Error('Не найден корневой элемент приложения');

createRoot(root).render(
  <StrictMode>
    <LabCatalog />
  </StrictMode>,
);
