import {defineConfig} from 'vite';
import {readFileSync, realpathSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
// Only explicitly referenced text files can be read; no general repository mount.
function repositoryFiles(server) {
  server.middlewares.use('/repository/', (req,res) => {
    try {
      const requested=decodeURIComponent((req.url||'').split('?')[0]).replace(/^\//,'');
      const allowed=['sources','contents'].flatMap(k=>JSON.parse(readFileSync(new URL(`./data/${k}.json`,import.meta.url),'utf8')).map(s=>s.path).filter(Boolean));
      if(!allowed.includes(requested)) {res.statusCode=404;res.end('Not found');return;}
      const root=realpathSync(fileURLToPath(new URL('../',import.meta.url)));
      const target=realpathSync(path.resolve(root,requested));
      if(!target.startsWith(root+path.sep)) {res.statusCode=403;res.end('Forbidden');return;}
      res.setHeader('Content-Type','text/plain; charset=utf-8');
      res.setHeader('X-Content-Type-Options','nosniff');
      res.end(readFileSync(target));
    } catch {res.statusCode=404;res.end('Not found');}
  });
}
export default defineConfig({plugins:[{name:'atlas-repository-references',configureServer:repositoryFiles,configurePreviewServer:repositoryFiles}]});
