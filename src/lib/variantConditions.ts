import type {Lab} from '../types'

// Use the resolved assignment, not a generic profile shared by all semesters.
export function variantConditions(lab:Lab):(string|number)[][] {
 const result:(string|number)[][]=[]
 for(const section of lab.sourceData.sections){
  const table=section.table;if(!table)continue
  if(section.title==='Параметры варианта')result.push(...table.rows)
  else if(table.columns.includes('variant')&&table.rows.length===1){
   table.columns.forEach((column,index)=>{if(column!=='variant')result.push([`${section.title} · ${column}`,table.rows[0][index]])})
  }
 }
 return result
}
