import fs from 'node:fs/promises'
import path from 'node:path'
const {labs}=JSON.parse(await fs.readFile('src/data/labs.json','utf8'))
for(const dir of ['brand','fonts'])await fs.cp('public/'+dir,'site-public/'+dir,{recursive:true})
await fs.copyFile('public/guide.html','site-public/guide.html')
await fs.mkdir('site-public/reports',{recursive:true})
for(const lab of labs)await fs.copyFile('public/reports/'+lab.reportFile,'site-public/reports/'+lab.reportFile)
for(const name of new Set(labs.flatMap(l=>l.standFiles))){
 let text=await fs.readFile(name,'utf8')
 if(name.endsWith('connection-cases.json'))text=JSON.stringify(JSON.parse(text).map(({fault,allowedChange,...rest})=>rest),null,2)
 const target=path.join('site-public',name);await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,text)
}
console.log('Synced',new Set(labs.flatMap(l=>l.standFiles)).size,'stand files')
