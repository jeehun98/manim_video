import Ajv from 'ajv';
import schema from '../data/schema.json' with { type: 'json' };
const validate = new Ajv({allErrors:true}).compile(schema);
export function validateAtlas(data) {
  if (!validate(data)) return validate.errors.map(e => `${e.instancePath || '/'} ${e.message}`);
  const errors = [];
  const sets = {};
  for (const key of ['concepts','relations','sources','contents']) {
    sets[key] = new Set();
    for (const item of data[key]) {
      if (sets[key].has(item.id)) errors.push(`${key}: duplicate id ${item.id}`);
      sets[key].add(item.id);
    }
  }
  for (const item of [...data.concepts,...data.relations]) for (const id of item.sourceIds) if (!sets.sources.has(id)) errors.push(`${item.id}: missing source ${id}`);
  for (const r of data.relations) {
    for (const id of [r.source,r.target]) if (!sets.concepts.has(id)) errors.push(`${r.id}: missing concept ${id}`);
    if (r.verificationStatus === 'verified' && (!r.sourceIds.length || r.provenance === 'ai_suggestion')) errors.push(`${r.id}: verification requires reviewed sources`);
  }
  for (const c of data.contents) for (const id of c.conceptIds) if (!sets.concepts.has(id)) errors.push(`${c.id}: missing concept ${id}`);
  for (const s of data.sources) {
    if (s.kind === 'repository' && !s.path) errors.push(`${s.id}: repository path required`);
    if (s.kind === 'external' && !/^https?:\/\//.test(s.url || '')) errors.push(`${s.id}: http(s) URL required`);
  }
  for (const item of [...data.sources,...data.contents]) if (item.path && (!/^(episodes|longforms|quantum_series|visual_library)\//.test(item.path) || item.path.split('/').includes('..') || item.path.includes('\\'))) errors.push(`${item.id}: unsafe repository path`);
  return errors;
}
