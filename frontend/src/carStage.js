import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/examples/jsm/loaders/DRACOLoader.js';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {classify} from './modelAdapters.js';

const BASE=import.meta.env.BASE_URL;
const RIMS={aero:['#4b4e53',1,.35],carbon:['#16171a',.6,.45],forged:['#cfd3d8',1,.12],performance:['#a07a45',1,.28]};
const LENGTH=4.5;                               
const VIEW_DIR=new THREE.Vector3(4.25,1.3,-4.6).normalize();

const CACHE=new Map(),ACTIVE=new Set(),MAX_CACHED=3;let loader;
const getLoader=()=>loader||(loader=new GLTFLoader().setDRACOLoader(new DRACOLoader().setDecoderPath(BASE+'draco/')));
function freeEntry(e){e.gl&&e.gl.scene.traverse(o=>{if(o.geometry)o.geometry.dispose();
 const orig=o.userData&&o.userData.orig;(Array.isArray(orig)?orig:orig?[orig]:[]).forEach(m=>{Object.values(m).forEach(t=>t&&t.isTexture&&t.dispose());m.dispose()})})}
export function loadModel(url){let e=CACHE.get(url);if(e){CACHE.delete(url);CACHE.set(url,e);return e.p}
 e={};e.p=new Promise((res,rej)=>getLoader().load(url,gl=>{e.gl=gl;res(gl)},undefined,rej));CACHE.set(url,e);
 e.p.then(()=>{while(CACHE.size>MAX_CACHED){const old=[...CACHE.keys()].find(u=>!ACTIVE.has(u)&&u!==url);if(!old)break;freeEntry(CACHE.get(old));CACHE.delete(old)}},()=>CACHE.delete(url));
 return e.p}

// ---- one-time preparation of a loaded GLB: classify parts, orient, scale, sit on the floor ----
function prepare(gl,cfg={}){if(gl.userData.prep)return gl.userData.prep;
 const root=gl.scene,holder=new THREE.Group(),slots=[],count={};holder.add(root);
 root.traverse(o=>{if(!o.isMesh)return;const chain=[];for(let p=o.parent;p&&chain.length<2;p=p.parent)chain.push(p.name);
  const orig=o.material,multi=Array.isArray(orig);o.userData.orig=orig;if(multi)o.material=[...orig];
  (multi?orig:[orig]).forEach((m,i)=>{const cls=classify({mesh:o.name,mat:m&&m.name,chain},cfg.adapter);if(cls){slots.push({o,i,multi,cls});count[cls]=(count[cls]||0)+1}})});
 const aero={};Object.entries(cfg.aero||{}).forEach(([part,res])=>{aero[part]=[];root.traverse(o=>{if(res.some(r=>r.test(o.name)))aero[part].push(o)})});
 const box=new THREE.Box3(),size=new THREE.Vector3(),ctr=new THREE.Vector3(),measure=()=>{root.updateMatrixWorld(true);box.setFromObject(root);box.getSize(size)};
 measure();if(size.x>size.z*1.05){root.rotation.y+=Math.PI/2;measure()}   // length axis -> Z
 if(cfg.rotY){root.rotation.y+=cfg.rotY;measure()}
 holder.scale.setScalar(LENGTH/size.z*(cfg.scale||1));holder.updateMatrixWorld(true);box.setFromObject(holder);box.getSize(size);box.getCenter(ctr);
 holder.position.set(-ctr.x,-box.min.y,-ctr.z);
 return gl.userData.prep={holder,slots,aero,count,w:size.x,h:size.y,l:size.z}}

export function createStage({preserve=false}={}){
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:preserve});
 renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.9;renderer.outputColorSpace=THREE.SRGBColorSpace;
 const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(36,1,.1,200);
 scene.environment=new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(),.04).texture;
 const cv=document.createElement('canvas');cv.width=cv.height=256;const g=cv.getContext('2d'),gr=g.createRadialGradient(128,128,10,128,128,128);
 gr.addColorStop(0,'rgba(0,0,0,.6)');gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(0,0,256,256);
 const shadow=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,depthWrite:false}));
 shadow.rotation.x=-Math.PI/2;shadow.position.y=.005;scene.add(shadow);
 const M={body:new THREE.MeshPhysicalMaterial({color:'#111',metalness:.75,roughness:.4,clearcoat:1,clearcoatRoughness:.03}),
  rim:new THREE.MeshStandardMaterial({metalness:1,roughness:.3}),caliper:new THREE.MeshStandardMaterial({metalness:.3,roughness:.4}),
  glass:new THREE.MeshPhysicalMaterial({color:'#fff',metalness:.25,roughness:0,transmission:1}),interior:new THREE.MeshStandardMaterial({roughness:.6}),
  badge:new THREE.MeshStandardMaterial({color:'#1b1c1e',metalness:.6,roughness:.4})};
 const s={renderer,scene,cam,M,cur:null,url:null,dist:9,ty:.45,look:null};
 s.setLook=look=>{s.look=look;M.body.color.set(look.body);const [c,m,r]=RIMS[look.wheelType]||RIMS.forged;M.rim.color.set(c);M.rim.metalness=m;M.rim.roughness=r;
  M.caliper.color.set(look.cal);M.interior.color.set(look.interior);
  if(s.cur)Object.entries(s.cur.aero).forEach(([part,list])=>list.forEach(o=>{o.visible=(look.parts||[]).includes(part)}))};
 s.show=(m,gl)=>{const p=prepare(gl,m.cfg);if(s.cur){scene.remove(s.cur.holder);ACTIVE.delete(s.url)}
  p.slots.forEach(({o,i,multi,cls})=>{if(multi)o.material[i]=M[cls];else o.material=M[cls]});
  scene.add(p.holder);s.cur=p;s.url=m.url;ACTIVE.add(m.url);
  s.dist=Math.max(p.l,p.h*2.2,p.w*1.2)*1.3*(m.cfg?.camera||1);s.ty=p.h*.45+(m.cfg?.targetY||0);shadow.scale.set(p.w*1.5,p.l*1.4,1);
  if(s.look)s.setLook(s.look);return p};
 s.home=ctl=>{cam.position.copy(VIEW_DIR).multiplyScalar(s.dist).add(new THREE.Vector3(0,s.ty,0));if(ctl){ctl.target.set(0,s.ty,0);ctl.update()}else cam.lookAt(0,s.ty,0)};
 s.resize=(w,h)=>{renderer.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()};
 s.dispose=()=>{if(s.cur){scene.remove(s.cur.holder);ACTIVE.delete(s.url)}Object.values(M).forEach(m=>m.dispose());renderer.dispose()};
 return s}

// ---- still image of a car (used for thumbnails: home, model picker, garage). One shared stage, requests queued, results cached ----
let snapStage,queue=Promise.resolve();const SNAPS=new Map();
export function snapshot(vehicle,look,w=1000,h=470){
 const key=[vehicle.key,look.body,look.wheelType,look.cal,look.interior,(look.parts||[]).join()].join('|');if(SNAPS.has(key))return SNAPS.get(key);
 const job=queue.then(async()=>{snapStage=snapStage||createStage({preserve:true});
  for(const m of vehicle.models){try{const gl=await loadModel(m.url);snapStage.show(m,gl);snapStage.setLook(look);snapStage.home();snapStage.resize(w,h);snapStage.renderer.render(snapStage.scene,snapStage.cam);
   return snapStage.renderer.domElement.toDataURL('image/png')}catch(e){/* try next candidate */}}return null});
 queue=job.catch(()=>{});SNAPS.set(key,job);return job}
