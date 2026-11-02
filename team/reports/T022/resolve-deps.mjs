import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const installed=createRequire('F:/Dropshipping/operations/launch-2026-10-05/theme-tools/package.json');
export async function resolve(specifier,context,nextResolve){
 try{return await nextResolve(specifier,context);}catch(error){
  if(error.code!=='ERR_MODULE_NOT_FOUND'||specifier.startsWith('.')||specifier.startsWith('/')||specifier.includes('://'))throw error;
  return nextResolve(pathToFileURL(installed.resolve(specifier)).href,context);
 }
}
