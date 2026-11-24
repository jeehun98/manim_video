import {readFileSync, existsSync} from 'node:fs';
import {validateAtlas} from '../src/validation.mjs';
import katex from 'katex';
const data = Object.fromEntries(['concepts','relations','sources','contents'].map(key => [key,JSON.parse(readFileSync(new URL(`../data/${key}.json`,import.meta.url),'utf8'))]));
const errors = validateAtlas(data);
for (const item of [...data.sources,...data.contents]) if (item.path && !existsSync(new URL('../../'+item.path, import.meta.url))) errors.push(`Missing repository file: ${item.path}`);
for (const n of data.concepts) if (n.formula) { try {katex.renderToString(n.formula,{throwOnError:true,trust:false});} catch(e) {errors.push(`${n.id}: ${e.message}`);} }
if(errors.length) { console.error(errors.join('\n')); process.exitCode=1; }
else console.log(`Atlas valid: ${data.concepts.length} concepts, ${data.relations.length} relations, ${data.sources.length} sources. Repository references and formulas checked.`);
