import React, {useEffect, useMemo, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import cytoscape, {type Core} from 'cytoscape';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import './style.css';
import concepts from '../data/concepts.json';
import relations from '../data/relations.json';
import sources from '../data/sources.json';
import contents from '../data/contents.json';
import {validateAtlas} from './validation.mjs';
import {visibleGraph} from './graph.mjs';
import {searchConcepts} from '../knowledge/retrieval.mjs';
import {type Atlas, type Concept, type Relation, colors, learningLabels, verificationLabels, relationLabels} from './model';

const atlas = {concepts, relations, sources, contents} as Atlas;
type Selection = {kind:'node'|'edge';id:string};
function App() {
  const [query,setQuery]=useState('');
  const [domain,setDomain]=useState(''); const [type,setType]=useState('');
  const [learning,setLearning]=useState(''); const [verification,setVerification]=useState('');
  const [focus,setFocus]=useState(''); const [depth,setDepth]=useState(1);
  const [selection,setSelection]=useState<Selection>({kind:'node',id:'fourier-series'});
  const [zoom,setZoom]=useState(100);
  const container=useRef<HTMLDivElement>(null); const graph=useRef<Core|null>(null);
  const errors=useMemo(()=>validateAtlas(atlas),[]);
  const visible=useMemo(()=>visibleGraph(atlas,{domain,type,learning,verification,focus,depth}),[domain,type,learning,verification,focus,depth]);
  const matches=searchConcepts(atlas,query) as Concept[];
  const node=selection.kind==='node'?atlas.concepts.find(n=>n.id===selection.id):undefined;
  const edge=selection.kind==='edge'?atlas.relations.find(r=>r.id===selection.id):undefined;
  const selectNode=(id:string)=>setSelection({kind:'node',id});
  const reset=()=>{setDomain('');setType('');setLearning('');setVerification('');setFocus('');setQuery('');};
  useEffect(()=>{
    if(!container.current || errors.length) return;
    const cy=cytoscape({container:container.current,elements:[],minZoom:.25,maxZoom:3, wheelSensitivity:.2,
      style:[
        {selector:'node',style:{'background-color':'data(color)','label':'data(label)','color':'#cbd5e1','font-size':13,'font-family':'Malgun Gothic, sans-serif','text-valign':'bottom','text-margin-y':11,'width':18,'height':18,'border-width':4,'border-color':'#1c2935','text-wrap':'wrap','text-max-width':'115px'}},
        {selector:'node[idea]',style:{'shape':'diamond','width':23,'height':23}},
        {selector:'edge',style:{'width':1.3,'line-color':'#3a4657','target-arrow-color':'#64748b','target-arrow-shape':'none','curve-style':'bezier','arrow-scale':.7,'overlay-padding':8}},
        {selector:'edge[directed]',style:{'target-arrow-shape':'triangle'}},
        {selector:'edge[status = "proposed"]',style:{'line-style':'dashed','line-color':'#667080'}},
        {selector:'edge[status = "verified"]',style:{'line-color':'#65c9c1'}},
        {selector:'edge[status = "rejected"]',style:{'line-color':'#bd6a77','line-style':'dotted'}},
        {selector:'.dim',style:{'opacity':.38}},
        {selector:'node.active',style:{'width':25,'height':25,'border-color':'#e2e8f0','border-width':3,'color':'#ffffff','font-weight':700}},
        {selector:'edge.active',style:{'line-color':'#c1ccdd','target-arrow-color':'#c1ccdd','width':2.5,'label':'data(label)','font-size':11,'color':'#eef2f8','text-background-color':'#151e29','text-background-opacity':1,'text-background-padding':'4px','text-rotation':'autorotate'}},
      ]});
    graph.current=cy;
    cy.on('tap','node',e=>setSelection({kind:'node',id:e.target.id()}));
    cy.on('tap','edge',e=>setSelection({kind:'edge',id:e.target.id()}));
    cy.on('zoom',()=>{
      setZoom(Math.round(cy.zoom()*100));
      // Keep labels readable when fitting the graph to a narrow viewport.
      cy.nodes().style('font-size',Math.min(36,13/cy.zoom()));
    });
    const observer=new ResizeObserver(()=>cy.resize()); observer.observe(container.current);
    return ()=>{observer.disconnect();cy.destroy();};
  },[errors]);
  useEffect(()=>{
    const cy=graph.current;if(!cy)return;
    const positions=new Map(cy.nodes().map(n=>[n.id(),n.position()]));
    cy.elements().remove();
    cy.add([
      ...visible.concepts.map((n:Concept)=>({data:{id:n.id,label:n.name,color:colors[n.domain]||'#91a8c3',...(n.type==='Idea'?{idea:1}:{})},position:positions.get(n.id)})),
      ...visible.relations.map((r:Relation)=>({data:{id:r.id,source:r.source,target:r.target,label:relationLabels[r.type],status:r.verificationStatus,...(r.directed?{directed:1}:{})}}))
    ]);
    cy.layout({name:'cose',animate:false,randomize:true,nodeDimensionsIncludeLabels:true,nodeRepulsion:()=>16000,idealEdgeLength:()=>140,padding:50,componentSpacing:100}).run();
  },[visible,errors]);
  useEffect(()=>{
    const cy=graph.current;if(!cy)return;
    cy.elements().removeClass('dim active');const selected=cy.getElementById(selection.id);
    if(selected.length){const neighborhood=selection.kind==='node'?selected.closedNeighborhood():selected.union(selected.connectedNodes());cy.elements().difference(neighborhood).addClass('dim');selected.addClass('active');}
  },[selection,visible]);
  const titleOf=(id:string)=>atlas.concepts.find(n=>n.id===id)?.name||id;
  function sourceList(ids:string[],locator?:string) {
    return ids.map(id=>{const s=atlas.sources.find(s=>s.id===id);return s?<div className="source" key={id}><strong>{s.title}</strong><span>{locator||s.locator}</span>{s.path?<a href={`/repository/${s.path}`} target="_blank" rel="noreferrer">보조 자료 열기 ↗</a>:<a href={s.url} target="_blank" rel="noreferrer">문헌 열기 ↗</a>}</div>:null;});
  }
  if(errors.length)return <main className="fatal"><h1>지식 데이터를 확인해 주세요</h1><pre>{errors.join('\n')}</pre></main>;
  return <div className="app">
    <header><div className="brand"><span className="brand-icon">⌘</span><div>Knowledge Atlas<small>SHARED KNOWLEDGE BASE</small></div></div><div className="header-note">AI와 사람이 함께 참조하는 지식 기반</div><span className="local-label">로컬 지식 기반</span></header>
    <div className="workspace">
      <aside className="sidebar"><div className="section-kicker">EXPLORE</div><h2>지식 탐색</h2><label className="search-label">개념 검색<input autoComplete="off" type="search" placeholder="이름, 별칭, ID, 설명 검색" value={query} onChange={e=>setQuery(e.target.value)}/></label>
        <div className="filters"><label>학문 분야<select value={domain} onChange={e=>setDomain(e.target.value)}><option value="">모든 분야</option>{[...new Set(atlas.concepts.map(n=>n.domain))].map(d=><option key={d}>{d}</option>)}</select></label>
        <label>관계 유형<select value={type} onChange={e=>setType(e.target.value)}><option value="">모든 관계</option>{Object.entries(relationLabels).map(([id,name])=><option key={id} value={id}>{name}</option>)}</select></label>
        <label>나의 학습 상태<select value={learning} onChange={e=>setLearning(e.target.value)}><option value="">모든 학습 상태</option>{Object.entries(learningLabels).map(([id,name])=><option key={id} value={id}>{name}</option>)}</select></label>
        <label>관계 검증 상태<select value={verification} onChange={e=>setVerification(e.target.value)}><option value="">모든 검증 상태</option>{Object.entries(verificationLabels).map(([id,name])=><option key={id} value={id}>{name}</option>)}</select></label></div>
        <div className="list-heading"><span>개념 인덱스</span><span>{matches.length}</span></div>
        <div className="concept-list">{matches.length?matches.map(n=><button key={n.id} className={selection.id===n.id?'concept chosen':'concept'} onClick={()=>{selectNode(n.id);if(focus)setFocus(n.id);}}><i style={{background:colors[n.domain]||'#91a8c3'}}/><span>{n.name}<small>{n.domain}</small></span></button>):<p className="muted">검색 결과가 없습니다.</p>}</div>
        <button className="reset" onClick={reset}>검색·필터 초기화</button><p className="sidebar-foot">개념보다 연결의 이유를 기록합니다.<br/>선의 개수는 중요도의 척도가 아닙니다.</p>
      </aside>
      <main className="graph-panel"><div className="graph-heading"><div><span className="section-kicker">KNOWLEDGE GRAPH</span><h1>{focus?`${titleOf(focus)} 주변 탐색`:'아이디어 사이의 연결'}</h1></div><span className="count">{visible.concepts.length} 개념 / {visible.relations.length} 관계</span></div>
        <div className="graph-toolbar"><div className="segmented"><button className={!focus?'selected':''} onClick={()=>setFocus('')}>전체 구조</button><button className={focus?'selected':''} disabled={!node} onClick={()=>node&&setFocus(node.id)}>선택 개념 중심</button></div><label>연결 깊이 <select aria-label="연결 깊이" value={depth} onChange={e=>setDepth(Number(e.target.value))}>{[1,2,3].map(n=><option key={n} value={n}>{n}단계</option>)}</select></label></div>
        <div className="graph-canvas" ref={container} role="img" aria-label="개념과 관계 네트워크. 왼쪽 개념 목록과 오른쪽 관련 관계 목록으로도 탐색할 수 있습니다."/>
        {!visible.concepts.length&&<div className="empty"><h2>조건에 맞는 연결이 없습니다</h2><p>필터를 바꾸거나 전체 구조로 돌아가 보세요.</p><button onClick={reset}>전체 보기</button></div>}
        <div className="graph-bottom"><div className="legend">{Object.entries(colors).map(([d,c])=><span key={d}><i style={{background:c}}/>{d}</span>)}<span className="dash-legend">┄ 탐구 후보</span></div><div className="zoom"><button aria-label="축소" onClick={()=>graph.current?.zoom({level:(graph.current?.zoom()||1)/1.2,renderedPosition:{x:(container.current?.clientWidth||0)/2,y:(container.current?.clientHeight||0)/2}})}>−</button><span>{zoom}%</span><button aria-label="확대" onClick={()=>graph.current?.zoom({level:(graph.current?.zoom()||1)*1.2,renderedPosition:{x:(container.current?.clientWidth||0)/2,y:(container.current?.clientHeight||0)/2}})}>+</button><button onClick={()=>graph.current?.fit(undefined,65)}>맞춤</button></div></div>
        <div className="graph-help">노드를 끌어 배치 · 빈 공간을 끌어 이동 · 휠로 확대 · 연결선을 눌러 근거 확인</div>
      </main>
      <aside className="details" aria-live="polite"><div className="section-kicker">{node?'CONCEPT NOTES':'RELATION NOTES'}</div>
      {node&&<><div className="detail-meta"><span>{node.type}</span><span>{node.domain}</span></div><h2>{node.name}</h2><p className="description">{node.description}</p><div className="badge">{learningLabels[node.learningStatus]}</div>
        {node.formula&&<div className="formula" dangerouslySetInnerHTML={{__html:katex.renderToString(node.formula,{throwOnError:false,trust:false,displayMode:true})}}/>}
        <section><h3>연결된 관계</h3>{atlas.relations.filter(r=>r.source===node.id||r.target===node.id).map(r=><button className="relation-row" key={r.id} onClick={()=>setSelection({kind:'edge',id:r.id})}><span>{relationLabels[r.type]}<small>{verificationLabels[r.verificationStatus]}</small></span><strong>{titleOf(r.source===node.id?r.target:r.source)}<small>{r.directed?`${titleOf(r.source)} → ${titleOf(r.target)}`:'방향 없는 관계'}</small></strong></button>)}</section>
        {node.aliases?.length>0&&<p className="muted">별칭: {node.aliases.join(' · ')}</p>}<Questions questions={node.questions}/><section><h3>문헌·근거 자료</h3>{node.sourceIds.length?sourceList(node.sourceIds):<p>탐구 관점으로 등록한 노드입니다. 직접 근거는 아직 등록되지 않았습니다.</p>}</section>{atlas.contents.some(c=>c.conceptIds.includes(node.id))&&<section><h3>관련 출력물·보조 자료</h3>{atlas.contents.filter(c=>c.conceptIds.includes(node.id)).map(c=><div className="source" key={c.id}><strong>{c.title}</strong><span>{c.status==='script_present'?'대본 파일 확인':c.status}</span><a href={`/repository/${c.path}`} target="_blank" rel="noreferrer">제작 자료 열기 ↗</a><small>{c.note}</small></div>)}</section>}
      </>}
      {edge&&<><div className="detail-meta"><span>{relationLabels[edge.type]}</span><span className={'status '+edge.verificationStatus}>{verificationLabels[edge.verificationStatus]}</span></div><h2 className="edge-title"><button onClick={()=>selectNode(edge.source)}>{titleOf(edge.source)}</button><span>{edge.directed?'→':'↔'}</span><button onClick={()=>selectNode(edge.target)}>{titleOf(edge.target)}</button></h2><p className="description">{edge.description}</p><section><h3>성립 조건</h3><p>{edge.conditions}</p></section><section><h3>근거와 설명</h3><p>{edge.evidence}</p></section><section><h3>한계 및 미확인 사항</h3><p>{edge.limitations}</p></section><Questions questions={edge.questions}/>{edge.reviewNote&&<section><h3>검토 기록</h3><p>{edge.reviewNote}</p></section>}<section><h3>참고 자료</h3>{sourceList(edge.sourceIds,edge.sourceLocator)}</section><p className="muted">기록 유래: {edge.provenance}<br/>검증 상태와 나의 이해 상태는 별개입니다.</p></>}
      {!visible.concepts.some((n:Concept)=>n.id===node?.id)&&node&&<p className="notice">선택한 개념은 현재 그래프 필터 밖에 있습니다.</p>}
      <div className="editor-note">기록 수정은 data/ JSON 파일에서 합니다. 이 화면은 저장된 연구 기록을 탐색합니다.</div>
      </aside>
    </div><footer><span>KNOWLEDGE ATLAS <b> / </b> Graph View</span><span>{atlas.concepts.length}개 개념 · {atlas.relations.filter(r=>r.verificationStatus==='verified').length}개 관계 근거 확인 · CLI와 동일 지식 기반</span></footer>
  </div>;
}
function Questions({questions}:{questions:string[]}){return questions.length?<section><h3>탐구 질문</h3>{questions.map(q=><p className="question" key={q}>{q}</p>)}</section>:null;}
createRoot(document.getElementById('root')!).render(<App/>);
