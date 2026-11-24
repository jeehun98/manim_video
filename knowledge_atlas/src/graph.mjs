// Shared, pure graph queries: all future views can use the same records.
export function visibleGraph(data, filters) {
  const concepts = data.concepts.filter(n => (!filters.domain || n.domain === filters.domain) && (!filters.learning || n.learningStatus === filters.learning));
  const allowed = new Set(concepts.map(n => n.id));
  let relations = data.relations.filter(r => allowed.has(r.source) && allowed.has(r.target) && (!filters.type || r.type === filters.type) && (!filters.verification || r.verificationStatus === filters.verification));
  let nodes = concepts;
  if (filters.type || filters.verification) {
    const incident = new Set(relations.flatMap(r => [r.source, r.target]));
    nodes = concepts.filter(n => incident.has(n.id));
  }
  if (filters.focus) {
    const reached = new Set(allowed.has(filters.focus) ? [filters.focus] : []);
    for (let i = 0; i < filters.depth; i++) {
      const next = new Set(reached);
      for (const r of relations) if (reached.has(r.source) || reached.has(r.target)) { next.add(r.source); next.add(r.target); }
      for (const id of next) reached.add(id);
    }
    nodes = nodes.filter(n => reached.has(n.id));
    relations = relations.filter(r => reached.has(r.source) && reached.has(r.target));
  }
  return {concepts:nodes, relations};
}
