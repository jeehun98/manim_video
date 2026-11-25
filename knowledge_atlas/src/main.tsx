import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import concepts from '../data/concepts.json';
import {searchConcepts} from '../knowledge/retrieval.mjs';
import type {Concept} from './model';
import './style.css';

const inventory = {concepts};
const domains = [...new Set(concepts.map(concept => concept.domain))]
  .sort((a, b) => a.localeCompare(b, 'ko'));

function App() {
  const [query, setQuery] = useState('');
  const [domain, setDomain] = useState('');
  const matches: Concept[] = searchConcepts(inventory, query, {domain});
  const groups = new Map<string, Concept[]>();
  for (const concept of matches) {
    const group = groups.get(concept.domain) ?? [];
    group.push(concept);
    groups.set(concept.domain, group);
  }

  return (
    <main>
      <header>
        <h1>Knowledge Atlas</h1>
        <p>수학·물리 키워드 목록</p>
      </header>

      <div className="filters">
        <label>
          키워드 검색
          <input
            type="search"
            placeholder="예: 솔리톤, Fourier, PDE"
            value={query}
            onChange={event => setQuery(event.target.value)}
          />
        </label>
        <label>
          분야
          <select value={domain} onChange={event => setDomain(event.target.value)}>
            <option value="">전체 분야</option>
            {domains.map(name => <option key={name}>{name}</option>)}
          </select>
        </label>
      </div>

      <p className="result-count" role="status">
        {matches.length === concepts.length
          ? `전체 ${concepts.length}개`
          : `전체 ${concepts.length}개 중 ${matches.length}개`}
      </p>
      {matches.length === 0 && <p className="empty">일치하는 키워드가 없습니다.</p>}

      {domains.map(name => {
        const group = groups.get(name);
        if (!group) return null;
        return (
          <section key={name}>
            <h2>{name}</h2>
            <ul>
              {group.map(concept => (
                <li key={concept.id}>
                  <div className="term">
                    <strong>{concept.name}</strong>
                    <span lang="en">{concept.aliases.find(alias => /^[a-z]/i.test(alias))}</span>
                  </div>
                  <p>{concept.description}</p>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
