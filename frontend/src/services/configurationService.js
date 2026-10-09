import {request} from './api.js';
export const createConfiguration=payload=>request('/api/configurations',{method:'POST',body:payload});
export const getConfigurations=()=>request('/api/configurations');
export const getSharedBuild=buildId=>request(`/api/configurations/build/${encodeURIComponent(buildId)}`);
export const updateConfiguration=(id,payload)=>request(`/api/configurations/${id}`,{method:'PUT',body:payload});
export const deleteConfiguration=id=>request(`/api/configurations/${id}`,{method:'DELETE'});
