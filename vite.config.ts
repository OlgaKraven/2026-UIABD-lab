import react from '@vitejs/plugin-react'
import {defineConfig} from 'vite'
export default defineConfig({publicDir:'site-public',base:'/2026-UIABD-lab/',plugins:[react()],server:{host:'127.0.0.1'}})
