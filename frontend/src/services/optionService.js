import {request} from './api.js';
let cache=null;
export const getOptions=({refresh=false}={})=>{if(!cache||refresh)cache=request('/api/options',{auth:false}).catch(e=>{cache=null;throw e});return cache};
