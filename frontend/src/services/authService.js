import {request,tokenStore} from './api.js';
export const login=async({email,password})=>{const r=await request('/api/auth/login',{method:'POST',body:{email,password},auth:false});tokenStore.set(r.access_token);return r.user};
export const register=({email,username,password})=>request('/api/auth/register',{method:'POST',body:{email,username,password},auth:false});
export const getCurrentUser=()=>request('/api/auth/me');
export const logout=()=>tokenStore.clear();
export const hasToken=()=>!!tokenStore.get();
