import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loadAtlas} from '../knowledge/store.mjs';
import {visibleGraph} from '../src/graph.mjs';
import {validateAtlas} from '../src/validation.mjs';
const data=loadAtlas();
test('neighborhood expands one hop at a time, including incoming edges',()=>{
 const one=visibleGraph(data,{focus:'inner-product-space',depth:1});
 assert(one.concepts.some(n=>n.id==='vector-space'));
 assert(one.concepts.some(n=>n.id==='hilbert-space'));
 assert(!one.concepts.some(n=>n.id==='fourier-series'));
 assert(visibleGraph(data,{focus:'inner-product-space',depth:2}).concepts.some(n=>n.id==='fourier-series'));
});
test('filters never leave dangling graph edges',()=>{
 for (const filters of [{domain:'해석학'},{type:'specialization'},{verification:'proposed'},{learning:'understood'}]) {
  const g=visibleGraph(data,filters), ids=new Set(g.concepts.map(n=>n.id));
  assert(g.relations.every(r=>ids.has(r.source)&&ids.has(r.target)));
 }
 assert(visibleGraph(data,{verification:'verified'}).relations.every(r=>r.verificationStatus==='verified'));
});
test('rejects duplicate IDs, dangling references and automatically verified AI claims',()=>{
 const bad=structuredClone(data); bad.concepts.push(bad.concepts[0]); bad.relations[0].target='missing'; bad.relations[0].verificationStatus='verified';bad.relations[0].provenance='ai_suggestion';
 const errors=validateAtlas(bad).join(' ');
 assert.match(errors,/duplicate id/);assert.match(errors,/missing concept/);assert.match(errors,/reviewed sources/);
});
test('schema rejects invalid states and unsafe paths',()=>{
 const bad=structuredClone(data);bad.concepts[0].learningStatus='done';assert(validateAtlas(bad).length);
 const badPath=structuredClone(data);badPath.sources[0].path='episodes/../../secrets';assert(validateAtlas(badPath).length);
});
