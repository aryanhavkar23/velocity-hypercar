// Packs a .gltf (+ its .bin and textures) into ONE .glb in the backend's model folder.
// Usage (from frontend/):  npm run convert -- "path/to/scene.gltf" suzuki-swift
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import gltfPipeline from 'gltf-pipeline';
const [input,slug]=process.argv.slice(2);
if(!input||!slug){console.error('Usage: npm run convert -- <file.gltf> <car-slug>');process.exit(1)}
const out=path.join(path.dirname(fileURLToPath(import.meta.url)),'..','..','assets','models',`${slug}.glb`);
const gltf=JSON.parse(fs.readFileSync(input,'utf8'));
const {glb}=await gltfPipeline.gltfToGlb(gltf,{resourceDirectory:path.dirname(path.resolve(input))});
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,glb);
console.log(`Wrote ${out} (${(glb.length/1048576).toFixed(1)} MB)`);
