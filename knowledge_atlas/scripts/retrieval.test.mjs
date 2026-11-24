import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,readFileSync,unlinkSync,rmdirSync} from 'node:fs';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {loadAtlas,upsertRecord} from '../knowledge/store.mjs';
import {searchConcepts,searchRelations,searchSources,subgraph,findPaths,ideaCases,contextFor,visibleGraph,resolveConcept} from '../knowledge/retrieval.mjs';
const data=loadAtlas();
test('search uses aliases, domains and node types, not content presence',()=>{
 assert.equal(searchConcepts(data,'factorization theorem')[0].id,'factorization-theorem');
 assert(searchConcepts(data,'',{domain:'통계학',nodeType:'Theorem'}).some(n=>n.id==='factorization-theorem'));
 assert(!data.contents.some(c=>c.conceptIds.includes('factorization-theorem')));
 assert.equal(resolveConcept(data,'Hilbert space').id,'hilbert-space');
 assert(searchRelations(data,'완비성').some(r=>r.target==='hilbert-space'));
 assert(searchSources(data,'DLMF').length>=2);
});
test('direction and depth are explicit; reverse traversal does not invent implications',()=>{
 assert.equal(findPaths(data,'vector-space','hilbert-space',{type:'specialization'}).paths[0].relations.length,2);
 assert.equal(findPaths(data,'hilbert-space','vector-space',{type:'specialization'}).paths.length,0);
 const reverse=findPaths(data,'hilbert-space','vector-space',{type:'specialization',direction:'both'});
 assert(reverse.paths[0].steps.every(s=>s.againstDirection));
 assert.equal(findPaths(data,'vector-space','hilbert-space',{depth:1}).paths.length,0);
 assert.equal(findPaths(data,'vector-space','vector-space').paths[0].relations.length,0);
 assert.throws(()=>subgraph(data,'missing'),/Unknown/);
 assert.throws(()=>subgraph(data,'vector-space',{depth:-1}),/depth/);
});
test('context preserves claims, conditions, verification and source traceability',()=>{
 const result=contextFor(data,'hilbert-space',{depth:2});
 assert(result.relations.some(r=>r.verificationStatus==='proposed'));
 for(const r of result.relations){assert(r.conditions);assert(r.limitations);assert(r.verificationStatus);for(const id of r.sourceIds)assert(result.sources.some(s=>s.id===id));}
 assert(result.instructions.some(s=>s.includes('not a proof')));
 const budget=contextFor(data,'hilbert-space',{depth:3,maxChars:4500});
 assert(JSON.stringify(budget,null,2).length<=4500);
 assert(budget.metadata.truncated);assert.equal(budget.concepts[0].id,'hilbert-space');
 const ids=new Set(budget.concepts.map(n=>n.id));assert(budget.relations.every(r=>ids.has(r.source)&&ids.has(r.target)));
 const verified=contextFor(data,'hilbert-space',{depth:2,verification:'verified'});
 assert(verified.relations.every(r=>r.verificationStatus==='verified'));
});
test('rejected records are excluded from retrieval but available for explicit review',()=>{
 const fixture=structuredClone(data);fixture.relations[0].verificationStatus='rejected';
 assert(!subgraph(fixture,'vector-space').relations.some(r=>r.id===fixture.relations[0].id));
 assert(subgraph(fixture,'vector-space',{includeRejected:true}).relations.some(r=>r.id===fixture.relations[0].id));
 assert(visibleGraph(fixture,{verification:'rejected'}).relations.length);
 assert.throws(()=>ideaCases(data,'vector-space'),/not an Idea/);
 assert(ideaCases(data,'representation').concepts.some(n=>n.id==='fourier-series'));
});
test('standalone data loads and updates without contents or any Manim files',()=>{
 const directory=mkdtempSync(path.join(tmpdir(),'atlas-test-'));
 try{
  for(const key of ['concepts','relations','sources'])writeFileSync(path.join(directory,key+'.json'),JSON.stringify(data[key]));
  const standalone=loadAtlas(directory);assert.equal(standalone.contents.length,0);
  assert(searchConcepts(standalone,'Hilbert').length);
  const node={...standalone.concepts[0],aliases:[...standalone.concepts[0].aliases,'test-alias']};
  assert.equal(upsertRecord('concepts',node,directory).operation,'replaced');
  assert.equal(resolveConcept(loadAtlas(directory),'test-alias').id,node.id);
  const file=path.join(directory,'relations.json'),before=readFileSync(file,'utf8');
  assert.throws(()=>upsertRecord('relations',{...data.relations[0],target:'missing'},directory),/Update rejected/);
  assert.equal(readFileSync(file,'utf8'),before);
 }finally{
  for(const key of ['concepts','relations','sources'])unlinkSync(path.join(directory,key+'.json'));
  rmdirSync(directory);
 }
});
