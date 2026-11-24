import {readFileSync, existsSync, writeFileSync, renameSync, unlinkSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {validateAtlas} from './validation.mjs';
export const defaultDataDirectory=fileURLToPath(new URL('../data/',import.meta.url));
export function loadAtlas(directory=defaultDataDirectory) {
  const data={};
  for(const key of ['concepts','relations','sources','contents']) {
    const file=path.join(directory,`${key}.json`);
    data[key]=key==='contents'&&!existsSync(file)?[]:JSON.parse(readFileSync(file,'utf8').replace(/^\uFEFF/,''));
  }
  const errors=validateAtlas(data);
  if(errors.length)throw new Error(`Invalid knowledge data:\n${errors.join('\n')}`);
  return data;
}
export function upsertRecord(collection,record,directory=defaultDataDirectory) {
  if(!['concepts','relations','sources','contents'].includes(collection))throw new Error('Unknown collection');
  const data=loadAtlas(directory);
  const index=data[collection].findIndex(item=>item.id===record.id);
  if(index<0)data[collection].push(record);else data[collection][index]=record;
  const errors=validateAtlas(data);
  if(errors.length)throw new Error(`Update rejected; files unchanged:\n${errors.join('\n')}`);
  const destination=path.join(directory,`${collection}.json`),temporary=destination+`.${process.pid}.tmp`;
  try {
    writeFileSync(temporary,JSON.stringify(data[collection],null,2)+'\n',{encoding:'utf8',flag:'wx'});
    renameSync(temporary,destination);
  } finally {if(existsSync(temporary))unlinkSync(temporary);}
  return {collection,id:record.id,operation:index<0?'added':'replaced'};
}
