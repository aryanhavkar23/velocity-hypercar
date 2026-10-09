// Prints the node + material names of every GLB in ../assets/models (use it to tune adapters). Usage: node scripts/inspect-models.mjs
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const dir=process.argv[2]||path.join(path.dirname(fileURLToPath(import.meta.url)),'..','..','assets','models');
if(!fs.existsSync(dir)){console.error('No GLBs yet in assets/models');process.exit(1)}
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.glb'))){const b=fs.readFileSync(path.join(dir,f)),len=b.readUInt32LE(12),j=JSON.parse(b.slice(20,20+len).toString());
console.log(`\n=== ${f}  (${(b.length/1048576).toFixed(1)} MB)\nmaterials: ${(j.materials||[]).map(m=>m.name).join(' | ')}\nnodes: ${(j.nodes||[]).map(n=>n.name).filter(Boolean).slice(0,120).join(' | ')}`)}
