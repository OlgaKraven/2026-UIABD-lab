import fs from 'node:fs/promises'
import assert from 'node:assert/strict'
const read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''))
const {labs}=await read('src/data/labs.json'),old=await read('authoring/original-labs.json'),datasets=await read('src/data/datasets.json')
assert.equal(labs.length,22);assert.equal(new Set(labs.map(l=>l.slug)).size,22)
const totals={};let combinations=0
for(const source of old){
 const lab=labs.find(l=>l.slug===source.id);assert(lab)
 for(const key of ['number','title','semester'])assert.equal(lab[key],source[key],`${source.id}:${key}`)
 assert.equal(lab.blockTitle,source.block);assert.equal(lab.topicTitle,source.lectureTopic.title)
 assert.equal(lab.points,source.lms.rubric.reduce((n,r)=>n+r.points,0));assert.equal(lab.points,lab.rubric.reduce((n,r)=>n+r.points,0))
 totals[lab.semester]=(totals[lab.semester]||0)+lab.points
 await fs.access('public/reports/'+lab.reportFile)
 for(const file of lab.standFiles)await fs.access(file)
 for(let variant=1;variant<=30;variant++){
  const data=datasets[lab.slug][variant];assert(data);assert(data.conditions.table.rows.some(([k,v])=>k==='variant'&&Number(v)===variant));combinations++
  for(const section of [...lab.sourceData.sections,...data.sections])if(section.table){const {columns,rows}=section.table;assert(columns.length);for(const row of rows)assert.equal(row.length,columns.length,section.title)}
 }
}
const publicText=JSON.stringify({labs,datasets});assert(!/https?:[^"\s]*lecture/i.test(publicText));assert(!/durationAcademicHours|ориентир \d+ минут|на выполнение[^"\n]{0,30}\d+ час/i.test(publicText))
assert.equal(combinations,660);assert.deepEqual(totals,{6:70,7:100,8:50})
const report={labs:22,variants:30,combinations,totals,protectedIdentity:true,studentLectureLinks:0,studentTimeBudgets:0}
await fs.writeFile('quality/content-check.json',JSON.stringify(report,null,2));console.log(report)
