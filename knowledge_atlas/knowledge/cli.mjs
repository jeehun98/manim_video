#!/usr/bin/env node
import {readFileSync} from 'node:fs';
import {parseArgs} from 'node:util';
import {loadAtlas,upsertRecord} from './store.mjs';
import {searchConcepts,searchRelations,searchSources,subgraph,findPaths,ideaCases,contextFor} from './retrieval.mjs';
const help=`Knowledge Atlas — independent knowledge retrieval (JSON output)
node knowledge_atlas/knowledge/cli.mjs <command> [arguments] [options]

search [query]               Search names, aliases, tags and descriptions
relations [query]            Search relation claims, conditions and evidence
sources [query]              Search source metadata
neighbors <id/name/alias>    Extract a bounded neighborhood
paths <from> <to>            Shortest graph paths within the depth bound
ideas <idea-id>              Find cases attached to an Idea
context <id/name/alias>      AI context with complete conditions and citations
validate                    Validate data without browser or Manim files
upsert <collection> --file record.json   Validate and add/replace one full record

Options:
--domain <name> --node-type <type>   Concept search filters
--type <relation-type> --status <state>  Relation traversal filters
--depth <0..8> --direction <in|out|both> --limit <1..50>
--max-nodes <1..1000> --max-chars <1000..200000>
--include-rejected          Include rejected relations explicitly
--data <directory>          Use another standalone data directory

Neighbors/context default: depth 1, direction both. Paths: depth 4, direction out.
Rejected relations are excluded by default. Graph paths are not proofs.
No AI API is called; output must be read or passed to the model explicitly.
`;
try {
  const {values:v,positionals:p}=parseArgs({allowPositionals:true,options:{
    help:{type:'boolean'},data:{type:'string'},domain:{type:'string'},'node-type':{type:'string'},
    type:{type:'string'},status:{type:'string'},depth:{type:'string'},direction:{type:'string'},limit:{type:'string'},
    'max-nodes':{type:'string'},'max-chars':{type:'string'},'include-rejected':{type:'boolean'},file:{type:'string'}
  }});
  if(v.help||!p.length){console.log(help);process.exit(0);}
  const [command,...args]=p;
  const required={search:0,relations:0,sources:0,neighbors:1,paths:2,ideas:1,context:1,validate:0,upsert:1};
  if(!(command in required))throw new Error(`Unknown command: ${command}. Use --help.`);
  if(args.length<required[command])throw new Error(`${command} needs ${required[command]} argument(s).`);
  if(args.length>(['search','relations','sources'].includes(command)?1:required[command]))throw new Error('Unexpected positional argument; quote search phrases.');
  const filters={domain:v.domain,nodeType:v['node-type'],type:v.type,verification:v.status,direction:v.direction,includeRejected:v['include-rejected']||v.status==='rejected'};
  for(const [flag,key,min,max] of [['depth','depth',0,8],['limit','limit',1,50],['max-nodes','maxNodes',1,1000],['max-chars','maxChars',1000,200000]])if(v[flag]!==undefined){
    const n=Number(v[flag]);if(!/^\d+$/.test(v[flag])||!Number.isInteger(n)||n<min||n>max)throw new Error(`--${flag} must be ${min}..${max}`);filters[key]=n;
  }
  const data=loadAtlas(v.data);
  if(v.status&&!['proposed','investigating','verified','rejected'].includes(v.status))throw new Error('Unknown verification status');
  if(v.type&&!['prerequisite','generalization','specialization','equivalence','isomorphism','representation','transformation','application','derivation','shared_strategy','analogy','related_to'].includes(v.type))throw new Error('Unknown relation type');
  if(v.direction&&!['in','out','both'].includes(v.direction))throw new Error('Unknown direction');
  let result;
  switch(command){
    case 'search':result={concepts:searchConcepts(data,args[0],filters)};break;
    case 'relations':result={relations:searchRelations(data,args[0],filters)};break;
    case 'sources':result={sources:searchSources(data,args[0])};break;
    case 'neighbors':result=subgraph(data,args[0],filters);break;
    case 'paths':result=findPaths(data,args[0],args[1],filters);break;
    case 'ideas':result=ideaCases(data,args[0],filters);break;
    case 'context':result=contextFor(data,args[0],filters);break;
    case 'validate':result={valid:true,concepts:data.concepts.length,relations:data.relations.length,sources:data.sources.length};break;
    case 'upsert':
      if(!v.file)throw new Error('upsert requires --file <full-record.json>');
      result=upsertRecord(args[0],JSON.parse(readFileSync(v.file,'utf8').replace(/^\uFEFF/,'')),v.data);break;
  }
  console.log(JSON.stringify(result,null,2));
}catch(error){console.error(error.message);process.exitCode=2;}
