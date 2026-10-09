
export const inr=n=>'₹'+Math.round(n||0).toLocaleString('en-IN');
export const short=n=>n>=1e7?`₹${(n/1e7).toFixed(2)} Cr`:`₹${(n/1e5).toFixed(2)} L`;
export const byId=(l,id)=>(l||[]).find(x=>x.id===id)||null;

export const LIGHTS=[{id:'signature',name:'Signature',color:'#ffffff'},{id:'shadow',name:'Shadow',color:'#2a2d31'},{id:'laser',name:'Laser',color:'#7fd6ff'},{id:'track',name:'Track',color:'#ffc77a'}];


export const SEL_KEYS=['car_id','paint_id','wheel_id','caliper_id','interior_material_id','interior_color_id','seat_type_id','engine_id','performance_package_id','aero_package_id'];

export const optionsForCar=(o,carId)=>Object.fromEntries(Object.entries(o).map(([k,l])=>[k,l.filter(x=>x.car_id==null||x.car_id===carId)]));
export const defaultSelection=(carId,all)=>{const o=optionsForCar(all,carId);return{car_id:carId,paint_id:o.paints[0]?.id,wheel_id:o.wheels[0]?.id,caliper_id:o.calipers[0]?.id,
interior_material_id:o.interior_materials[0]?.id,interior_color_id:o.interior_colors[0]?.id,seat_type_id:o.seat_types[0]?.id,
engine_id:o.engines[0]?.id,performance_package_id:o.performance_packages[0]?.id,aero_package_id:o.aero_packages[0]?.id}};

export const switchCar=(prev,carId,o)=>({...defaultSelection(carId,o),paint_id:prev.paint_id,wheel_id:prev.wheel_id,caliper_id:prev.caliper_id,interior_material_id:prev.interior_material_id,interior_color_id:prev.interior_color_id,seat_type_id:prev.seat_type_id});
export const selectionKey=s=>SEL_KEYS.map(k=>s[k]).join('-');
export const savePayload=(s,name)=>{const p={};SEL_KEYS.forEach(k=>{p[k]=s[k]});p.name=name;return p};
export const selectionFromBuild=b=>({car_id:b.car.id,paint_id:b.exterior.paint.id,wheel_id:b.exterior.wheels.id,caliper_id:b.exterior.caliper.id,
interior_material_id:b.interior.material.id,interior_color_id:b.interior.color.id,seat_type_id:b.interior.seat.id,
engine_id:b.performance.engine.id,performance_package_id:b.performance.package.id,aero_package_id:b.performance.aero.id});

const STYLES=['aero','carbon','forged','performance'];
export function wheelStyle(w,list){const n=String(w?.name||'').toLowerCase();const hit=STYLES.find(s=>n.includes(s));if(hit)return hit;
if(/alloy|forg/.test(n))return'forged';const i=Math.max(0,(list||[]).findIndex(x=>x.id===w?.id));return STYLES[i%STYLES.length]}

export function aeroParts(a){const t=`${a?.name||''} ${a?.description||''}`.toLowerCase(),p=[];
if(/splitter|lip/.test(t))p.push('splitter');if(/skirt/.test(t))p.push('skirts');if(/wing|spoiler/.test(t))p.push('wing');if(/diffuser/.test(t))p.push('diffuser');return p}

export function makeLook(o,s,lightsId='signature'){const paint=byId(o.paints,s.paint_id),w=byId(o.wheels,s.wheel_id),cal=byId(o.calipers,s.caliper_id),
ic=byId(o.interior_colors,s.interior_color_id),aero=byId(o.aero_packages,s.aero_package_id);
return{body:paint?.hex_code||'#111',paintName:paint?.name||'',cal:cal?.hex_code||'#e0202c',wheelType:wheelStyle(w,o.wheels),
light:(LIGHTS.find(l=>l.id===lightsId)||LIGHTS[0]).color,parts:aeroParts(aero),interior:ic?.hex_code||'#15161a'}}
export const pickPaint=(o,re)=>o.paints.find(p=>re.test(p.name))||o.paints[0];

const lineDefs=o=>s=>[[byId(o.paints,s.paint_id),'Paint'],[byId(o.wheels,s.wheel_id),'Wheels'],[byId(o.calipers,s.caliper_id),'Calipers'],
[byId(o.interior_materials,s.interior_material_id),'Trim'],[byId(o.interior_colors,s.interior_color_id),'Interior colour'],[byId(o.seat_types,s.seat_type_id),'Seats'],
[byId(o.engines,s.engine_id),'Engine'],[byId(o.performance_packages,s.performance_package_id),'Package'],[byId(o.aero_packages,s.aero_package_id),'Aero']];
const linesOf=(o,s)=>lineDefs(o)(s).filter(([x])=>x&&x.price_modifier>0).map(([x,l])=>({label:`${x.name} ${l}`,price:x.price_modifier}));

export function previewBuild(car,o,s){const e=byId(o.engines,s.engine_id)||{},p=byId(o.performance_packages,s.performance_package_id)||{},a=byId(o.aero_packages,s.aero_package_id)||{};
const lines=linesOf(o,s),options=lineDefs(o)(s).reduce((t,[x])=>t+(x?.price_modifier||0),0),n=v=>v||0;
return{source:'estimate',base:car.base_price,options,lines,price:car.base_price+options,
horsepower:car.horsepower+n(e.horsepower_modifier)+n(p.horsepower_modifier),
topSpeed:car.top_speed+n(e.top_speed_modifier)+n(p.top_speed_modifier)+n(a.top_speed_modifier),
zeroToHundred:Math.max(1,+(car.acceleration+n(e.acceleration_modifier)+n(p.acceleration_modifier)).toFixed(1)),
handling:Math.min(100,car.handling+n(e.handling_modifier)+n(p.handling_modifier)+n(a.handling_modifier)),
braking:Math.min(100,car.braking+n(e.braking_modifier)+n(p.braking_modifier)),downforce:n(a.downforce),drag:n(a.drag)}}

export function backendBuild(b,o){const s=selectionFromBuild(b),st=b.performance.stats,a=byId(o.aero_packages,s.aero_package_id)||{};
return{source:'backend',base:b.pricing.base_price,options:b.pricing.options_total,lines:linesOf(o,s),price:b.pricing.final_price,
horsepower:st.horsepower,topSpeed:st.top_speed,zeroToHundred:st.acceleration,handling:st.handling,braking:st.braking,downforce:a.downforce||0,drag:a.drag||0}}
