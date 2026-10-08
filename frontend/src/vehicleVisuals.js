// Single source of truth: backend car -> how it is shown. The BACKEND decides which car it is; this file only says
// where that car's 3D model lives and how to read it. Matching is exact (slug, then exact normalised name):
// a car is never shown with another car's model.
import {resolveAssetUrl,API_BASE_URL} from './services/api.js';

export const normalizeCarKey=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const BASE=import.meta.env.BASE_URL;

// One entry per backend car. `model` (all optional) tunes how its GLB is placed and read:
//   rotY    radians to turn the car if it faces the wrong way (Math.PI flips it)
//   scale   size correction after auto-fit            camera  distance multiplier       targetY  look-at height offset
//   adapter {body|rim|caliper|glass|interior|badge|ignore: [RegExp]}  part overrides for odd naming (find names with `npm run inspect`)
//   aero    {wing|splitter|skirts|diffuser: [RegExp]}  node names the aero package shows/hides
//   credit  text shown under the 3D view (author · source · licence)
const REGISTRY=[
 {key:'porsche-911-gt3-rs',alt:'Porsche 911 GT3 RS',art:'gt3rs',slugs:['porsche-911-gt3-rs'],names:['porsche-911-gt3-rs'],model:{credit:''}},
 {key:'suzuki-swift',alt:'Suzuki Swift',slugs:['suzuki-swift'],names:['suzuki-swift'],model:{credit:''}}];

const find=car=>{const slug=normalizeCarKey(car.slug),name=normalizeCarKey(car.name);
 return REGISTRY.find(r=>slug&&r.slugs.includes(slug))||REGISTRY.find(r=>name&&r.names.includes(name))||null};

export function resolveVehicleVisual(car){
 const c=car||{},entry=find(c),slug=entry?entry.slugs[0]:normalizeCarKey(c.slug||c.name),cfg=entry?.model||{},backendImage=resolveAssetUrl(c.image_url);
 // 3D candidates, in order: the backend's /assets/models/<slug>.glb, then a copy bundled in public/models/cars/<slug>.glb
 const models=[`${API_BASE_URL}/assets/models/${slug}.glb`,`${BASE}models/cars/${slug}.glb`].map(url=>({url,cfg,credit:cfg.credit}));
 return{models,key:entry?.key||slug||'unknown',alt:entry?.alt||c.name||'Vehicle',sources:backendImage?[backendImage]:[],art:entry?.art||null}}
