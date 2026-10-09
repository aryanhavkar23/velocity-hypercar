import {request} from './api.js';
let cache=null;
export const getCars=({refresh=false}={})=>{if(!cache||refresh)cache=request('/api/cars',{auth:false}).catch(e=>{cache=null;throw e});return cache};
export const getCar=id=>request(`/api/cars/${encodeURIComponent(id)}`,{auth:false});
