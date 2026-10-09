import React from 'react';
import {Wheel} from './Wheel.jsx';

const Defs=()=><defs>
<linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity=".5"/><stop offset=".35" stopColor="#fff" stopOpacity=".05"/><stop offset=".7" stopColor="#000" stopOpacity=".15"/><stop offset="1" stopColor="#000" stopOpacity=".5"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#2c3a48"/><stop offset=".5" stopColor="#0a0e13"/><stop offset="1" stopColor="#151c24"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="7"/></filter></defs>;
const Shadow=({w=350})=><ellipse cx="400" cy="268" rx={w} ry="12" fill="#000" opacity=".45" filter="url(#bl)"/>;
const Arch=({cx,r=57})=><circle cx={cx} cy="218" r={r} fill="#050506"/>;

const GLC="M104 226 L102 198 C102 186 110 178 128 173 L232 150 C262 144 282 128 304 98 C320 76 342 62 372 60 L560 60 C590 60 606 68 622 86 L688 160 C706 166 716 178 716 198 L716 226Z";
export function GlcArt({look,wheels}){const{body,cal,light,parts,wheelType}=look;
return <svg viewBox="0 0 800 300" role="img" aria-label="Mercedes-Benz GLC 300e"><Defs/><clipPath id="glcb"><path d={GLC}/></clipPath><Shadow w={310}/>
{parts.includes('diffuser')&&<path d="M650 218 L726 214 L730 232 L654 232Z" fill="#0b0b0c"/>}
{parts.includes('wing')&&<path d="M590 56 L668 62 L672 70 L596 66Z" fill="#0b0b0c" stroke={body} strokeWidth="2"/>}
<path d="M360 54 L572 54" stroke="#0b0b0c" strokeWidth="5" strokeLinecap="round"/>
<path d={GLC} fill={body}/><path d={GLC} fill="url(#sh)"/>
<g clipPath="url(#glcb)"><rect x="100" y="204" width="620" height="26" fill="#0b0b0c" opacity=".85"/><Arch cx={215} r={59}/><Arch cx={590} r={59}/>
<path d="M130 190 C260 164 420 156 700 176" stroke="#fff" strokeOpacity=".5" strokeWidth="2" fill="none"/></g>
<path d="M286 138 L314 96 C326 82 342 74 366 73 L452 73 L452 138Z" fill="url(#gl)"/>
<path d="M464 73 L566 73 C584 73 596 80 608 94 L650 138 L464 138Z" fill="url(#gl)"/>
<path d="M452 73 L464 73 L464 138 L452 138Z" fill={body}/><path d="M458 138 L460 210" stroke="#000" strokeOpacity=".4" strokeWidth="1.5"/><path d="M300 138 L296 206" stroke="#000" strokeOpacity=".3" strokeWidth="1.5"/>
<rect x="420" y="150" width="26" height="5" rx="2" fill="#0b0b0c" opacity=".8"/><rect x="622" y="150" width="24" height="12" rx="2" fill="#0b0b0c" opacity=".55"/>
<path d="M106 178 L170 168 L176 178 L110 190Z" fill={light}/><path d="M106 196 L150 196 L150 204 L106 204Z" fill="#0b0b0c"/>
<g transform="translate(120 190)"><circle r="7" fill="none" stroke="#bfc3c8" strokeWidth="1.2"/><path d="M0 0V-7M0 0L6 3.5M0 0L-6 3.5" stroke="#bfc3c8" strokeWidth="1.2"/></g>
<path d="M698 164 L714 170 L714 184 L702 180Z" fill="#ff2b2b"/>
{parts.includes('skirts')&&<path d="M262 216 L548 216 L540 227 L270 227Z" fill="#0b0b0c" stroke={body}/>}
{parts.includes('splitter')&&<path d="M96 222 L196 220 L200 230 L100 232Z" fill="#0b0b0c" stroke={body}/>}
<Wheel cx={215} type={wheelType} cal={cal}/><Wheel cx={590} type={wheelType} cal={cal}/></svg>}

const P911="M54 222 L52 202 C54 190 70 184 96 180 C140 172 188 160 236 146 C262 138 282 126 298 112 C320 90 348 74 394 70 C442 66 500 74 556 96 C606 116 660 124 716 132 C742 136 758 150 760 174 L760 222Z";
export function Gt3Art({look}){const{body,cal,light,parts,wheelType}=look;const big=parts.includes('wing');
return <svg viewBox="0 0 800 300" role="img" aria-label="Porsche 911 GT3 RS"><Defs/><clipPath id="g3b"><path d={P911}/></clipPath><Shadow/>
{parts.includes('diffuser')&&<path d="M684 214 L772 206 L776 228 L690 228Z" fill="#0b0b0c"/>}
{big?<g><path d="M672 132 L684 92 L692 92 L690 134Z" fill="#111"/><path d="M700 130 L708 96 L714 96 L712 132Z" fill="#111"/><path d="M630 84 L784 70 L788 100 L636 112Z" fill="#0b0b0c" stroke={body} strokeWidth="2.5"/></g>
:<path d="M690 130 C720 128 750 126 770 124 L772 136 C750 140 720 142 692 142Z" fill="#0b0b0c" stroke={body} strokeWidth="1.5"/>}
<path d={P911} fill={body}/><path d={P911} fill="url(#sh)"/>
<g clipPath="url(#g3b)"><rect x="50" y="206" width="715" height="20" fill="#000" opacity=".42"/><Arch cx={200} r={58}/><Arch cx={575} r={60}/>
<path d="M120 188 C230 168 330 152 440 148 C540 146 650 156 745 176" stroke="#fff" strokeOpacity=".5" strokeWidth="2" fill="none"/>
<path d="M232 150 L300 150 L292 212" stroke="#000" strokeOpacity=".3" strokeWidth="1.5" fill="none"/></g>
<path d="M304 126 C320 100 348 84 394 81 C438 78 486 86 528 102 L470 128Z" fill="url(#gl)"/><path d="M322 120 C338 100 362 90 392 88 L352 122Z" fill="#fff" opacity=".1"/>
<path d="M470 128 L474 150" stroke="#000" strokeOpacity=".35" strokeWidth="1.5"/><path d="M505 150 L560 146 L568 176 L512 180Z" fill="#050607"/>
<path d="M186 160 L226 152 L228 158 L190 166Z" fill="#0b0b0c"/>
<ellipse cx="104" cy="181" rx="16" ry="9" fill={light} stroke="#0b0b0c" strokeWidth="2"/>
<path d="M742 142 L756 148 L758 158 L744 154Z" fill="#ff2b2b"/>
{parts.includes('skirts')&&<path d="M246 214 L536 214 L528 225 L254 225Z" fill="#0b0b0c" stroke={body}/>}
{parts.includes('splitter')&&<path d="M40 218 L150 214 L158 226 L48 229Z" fill="#0b0b0c" stroke={body}/>}
<Wheel cx={200} type={wheelType} cal={cal}/><Wheel cx={575} type={wheelType} cal={cal}/></svg>}

// Unknown model with no photo: a neutral dashed outline that is explicitly labelled with THAT model's name.
export function NamedPlaceholder({name}){return <svg viewBox="0 0 800 300" role="img" aria-label={`${name} preview unavailable`}><Defs/><Shadow w={300}/>
<path d="M60 224 L58 200 C60 186 80 180 110 174 C190 158 250 138 300 100 C340 70 400 62 450 66 C520 72 580 100 640 126 C700 134 744 148 748 180 L748 224Z" fill="none" stroke="currentColor" strokeOpacity=".4" strokeWidth="2.5" strokeDasharray="10 8"/>
<circle cx="200" cy="218" r="46" fill="none" stroke="currentColor" strokeOpacity=".4" strokeWidth="2.5" strokeDasharray="6 6"/><circle cx="590" cy="218" r="46" fill="none" stroke="currentColor" strokeOpacity=".4" strokeWidth="2.5" strokeDasharray="6 6"/>
<text x="400" y="170" textAnchor="middle" fontSize="34" fontWeight="300" letterSpacing="3" fill="currentColor">{name}</text><text x="400" y="198" textAnchor="middle" fontSize="12" letterSpacing="4" fill="currentColor" opacity=".6">IMAGE UNAVAILABLE</text></svg>}

export const ART={glc:GlcArt,gt3rs:Gt3Art};
