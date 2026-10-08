import React,{useEffect,useRef} from 'react';
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {createStage,loadModel} from './carStage.js';

// Interactive 3D view of ONE backend car. `vehicle` = {key,name,models:[{url,cfg}]} from vehicleVisuals.js.
// Switching `vehicle` swaps the model; a version token makes a late response for a previously selected car harmless.
export default function Car3D({vehicle,look,view,onFail,onLoad,onBusy}){
 const host=useRef(),S=useRef({token:0});S.current.look=look;
 useEffect(()=>{const el=host.current;let raf;
  try{
   const st=createStage(),canvas=st.renderer.domElement;el.appendChild(canvas);canvas.style.cssText='width:100%;height:100%;display:block;touch-action:none;cursor:grab';
   const ctl=new OrbitControls(st.cam,canvas);ctl.enablePan=false;ctl.enableDamping=true;ctl.maxPolarAngle=Math.PI/2-.04;
   const resize=()=>st.resize(el.clientWidth||1,el.clientHeight||1);resize();const ro=new ResizeObserver(resize);ro.observe(el);
   const loop=()=>{raf=requestAnimationFrame(loop);ctl.update();st.renderer.render(st.scene,st.cam)};loop();
   view.current={reset:()=>st.home(ctl),
    zoom:f=>{const d=st.cam.position.clone().sub(ctl.target);st.cam.position.copy(ctl.target).add(d.setLength(THREE.MathUtils.clamp(d.length()/f,ctl.minDistance,ctl.maxDistance)))},
    rotate:()=>{const d=st.cam.position.clone().sub(ctl.target);d.applyAxisAngle(new THREE.Vector3(0,1,0),.6);st.cam.position.copy(ctl.target).add(d)}};
   Object.assign(S.current,{st,ctl});st.setLook(S.current.look);
   return()=>{S.current.token++;cancelAnimationFrame(raf);ro.disconnect();ctl.dispose();st.dispose();el.contains(canvas)&&el.removeChild(canvas);view.current=null;S.current.st=null}
  }catch(e){onFail()}},[]);

 useEffect(()=>{const {st,ctl}=S.current;if(!st)return;const token=++S.current.token;onBusy&&onBusy(true);
  (async()=>{for(const m of vehicle.models){
    try{const gl=await loadModel(m.url);if(token!==S.current.token)return;st.show(m,gl);
     ctl.minDistance=st.dist*.55;ctl.maxDistance=st.dist*1.9;st.home(ctl);onLoad&&onLoad(m);onBusy&&onBusy(false);
     if(import.meta.env.DEV)console.info(`[VELOCITY] backend car: ${vehicle.name}\n[VELOCITY] resolved model: ${m.url}`);return}
    catch(e){if(token!==S.current.token)return}}
   onBusy&&onBusy(false);onFail&&onFail()})()},[vehicle]);

 useEffect(()=>{S.current.st&&S.current.st.setLook(look)},[look]);
 return <div ref={host} className="c3d"/>}
