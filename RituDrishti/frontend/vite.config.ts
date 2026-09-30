import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
export default defineConfig(({mode}) => {
  const env=loadEnv(mode,process.cwd(),'');
  if(!env.REACT_APP_BACKEND_URL || !env.PORT) throw new Error('REACT_APP_BACKEND_URL and PORT are required');
  return {plugins:[react()],resolve:{alias:{'@':path.resolve(__dirname,'src')}},define:{'process.env.REACT_APP_BACKEND_URL':JSON.stringify(env.REACT_APP_BACKEND_URL)},server:{host:'0.0.0.0',port:Number(env.PORT),allowedHosts:true},build:{outDir:'build'}};
});