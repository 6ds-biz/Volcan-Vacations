const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
test('operational canvas adapters are retired and Website navigation is Owner scoped',()=>{assert(!fs.existsSync(path.join(root,'components/page-builder')));const source=fs.readFileSync(path.join(root,'components/ops-shell.tsx'),'utf8');assert(source.includes('website.manage'));assert(source.includes('/website/pages'));assert(source.includes('/website/media'));});
