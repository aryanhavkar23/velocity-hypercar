import React from 'react';
export function Wheel({cx,cy=218,type,cal,bare}){const n={aero:0,carbon:5,forged:10,performance:6}[type],w={carbon:8,forged:3,performance:6}[type],rim={aero:'#5a5d63',carbon:'#1d1e21',forged:'#c4c8ce',performance:'#a07a45'}[type];
return <g transform={`translate(${cx} ${cy})`}>{!bare&&<><circle r="50" fill="#0a0a0b"/><circle r="45" fill="none" stroke="#2a2a2d" strokeWidth="1.5"/></>}<circle r="37" fill="#6d7075"/><circle r="31" fill="none" stroke="#a5a8ad" strokeDasharray="2 3"/>
<rect x="12" y="-22" width="16" height="28" rx="4" fill={cal}/>
{type==='aero'?<><circle r="36" fill={rim}/><circle r="26" fill="none" stroke="#2a2c30" strokeWidth="3" strokeDasharray="7 5"/></>:Array.from({length:n},(_,i)=><rect key={i} x={-w/2} y="-35" width={w} height="31" fill={rim} transform={`rotate(${i*360/n})`} rx="1"/>)}
<circle r="36" fill="none" stroke={rim} strokeWidth="4"/><circle r="7" fill="#15161a" stroke={rim}/></g>}
