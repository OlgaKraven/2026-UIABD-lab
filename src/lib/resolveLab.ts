import payload from '../data/datasets.json'
import type {Lab,DataSection} from '../types'
const datasets=payload as Record<string,Record<string,{conditions:DataSection;sections:DataSection[]}>>
export function resolveLab(lab:Lab,variant:number):Lab {
 const data=datasets[lab.slug]?.[String(variant)]
 if(!data)throw Error(`Нет набора ${lab.slug}/${variant}`)
 const extraNames=new Set(data.sections.map(s=>s.title))
 const sections=lab.sourceData.sections.filter(s=>s.title!=='Параметры варианта'&&!extraNames.has(s.title)).map(section=>{
  if(section.table){const col=section.table.columns.indexOf('variant');if(col>=0)return {...section,table:{...section.table,rows:section.table.rows.filter(row=>Number(row[col])===variant)}}}
  if(section.title==='connection-cases.json'&&section.content){return {...section,content:[JSON.stringify(JSON.parse(section.content[0]).filter((r:{variant:number})=>r.variant===variant),null,2)]}}
  if(section.title==='kod-5-customers.json'&&section.content){const original=JSON.parse(section.content[0]);const code=String(variant).padStart(2,'0');return {...section,content:[JSON.stringify({...original,variants:{[code]:original.variants[code]}},null,2)]}}
  return section
 })
 return {...lab,sourceData:{...lab.sourceData,sections:[data.conditions,...sections,...data.sections]}}
}
