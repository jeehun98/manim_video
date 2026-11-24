import {existsSync} from 'node:fs';
import {loadAtlas} from '../knowledge/store.mjs';
import katex from 'katex';
const data = loadAtlas();
const errors = [];
if(process.argv.includes('--repository'))for (const item of [...data.sources,...data.contents]) if (item.path && !existsSync(new URL('../../'+item.path, import.meta.url))) errors.push(`Missing optional repository file: ${item.path}`);
for (const n of data.concepts) if (n.formula) { try {katex.renderToString(n.formula,{throwOnError:true,trust:false});} catch(e) {errors.push(`${n.id}: ${e.message}`);} }
if(errors.length) { console.error(errors.join('\n')); process.exitCode=1; }
else console.log(`Atlas valid: ${data.concepts.length} concepts, ${data.relations.length} relations, ${data.sources.length} sources. Formulas checked. Optional repository files ${process.argv.includes('--repository')?'checked':'not required'}.`);
