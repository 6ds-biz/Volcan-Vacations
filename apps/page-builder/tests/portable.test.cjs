const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const root = path.resolve(__dirname, '../../..');
const cache = new Map();
function load(file) {
  file = path.resolve(file);
  if (cache.has(file)) return cache.get(file);
  const result = {}; cache.set(file, result);
  const code = ts.transpileModule(fs.readFileSync(file, 'utf8'), {compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020}}).outputText;
  new Function('exports', 'require', code)(result, key => {
    if (key === '@6ds/page-builder/core') return load(path.join(root, 'packages/page-builder/src/core.ts'));
    if (key.startsWith('.')) return load(path.resolve(path.dirname(file), key + '.ts'));
    return require(key);
  });
  return result;
}
const core = load(path.join(root, 'packages/page-builder/src/core.ts'));
const portable = load(path.join(__dirname, '../src/portable.ts'));
const {vvDefinition: project} = load(path.join(__dirname, '../src/projects/vv/definition.ts'));
const serialize = (page, key = 'home') => portable.serializeLayout(page, project, key);
const parse = (raw, key = 'home') => portable.parseLayout(raw, project, key);
const hero = page => page.sections[0].columns[0].widgets[0];

test('six source defaults validate and round trip deterministically', () => {
  assert.equal(project.pages.length, 6);
  for (const {id} of project.pages) {
    const page = project.defaults(id), raw = serialize(page, id);
    assert.deepEqual(parse(raw, id), page);
    assert.equal(serialize(parse(raw, id), id), raw);
    assert(!/retail_price|supplier|credential|password|customer|availability_data|base64/i.test(raw));
  }
  assert.deepEqual(project.defaults('home').sections.map(s => s.columns[0].widgets[0].type), ['hero','arenal-feature','featured-experiences','benefits','trip-planning','pacific-coast','coastal-destinations','kinds-of-adventure','how-it-works','final-cta']);
});
test('edit, media replacement, responsive crop, export and import retain all design data', () => {
  const page = project.defaults('home');
  hero(page).config = {heading: 'Your Costa Rica adventure', eyebrow: 'Discover', copy: 'Made for you', subheadline: 'Explore at your pace', label: 'Start planning', href: '/plan-your-trip', surface: 'charcoal', accent: 'gold-light', typography: 'heading', space: 'xl', media: {...structuredClone(core.mediaDefaults), asset: 'vv-papagayo', x: 37, y: 63, overlay: 'dark', tablet: {asset: 'vv-nosara', x: 72}, mobile: {y: 20}}};
  hero(page).responsive.tablet = {width: 8, align: 'center', spacing: 'large'};
  hero(page).responsive.mobile = {visible: false, width: 12, order: 3};
  const raw = serialize(page);
  assert.equal(JSON.parse(raw).sections[0].columns[0].widgets[0].config.media.x, .37);
  assert.deepEqual(parse(raw), page);
  assert.equal(serialize(parse(raw)), raw);
});
test('invalid JSON, schema, project, page and root configuration fail clearly', () => {
  assert.throws(() => parse('{'), /Invalid JSON/);
  for (const [key, value, pattern] of [['schema_version', 2, /schema version/], ['project', 'nova', /different project/], ['page_type', 'about', /Select that page/], ['customer', {}, /configuration/]]) {
    const layout = JSON.parse(serialize(project.defaults('home'))); layout[key] = value;
    assert.throws(() => parse(JSON.stringify(layout)), pattern);
  }
});
test('invalid nesting, widgets, responsive settings and duplicate identifiers fail', () => {
  for (const mutate of [p => p.sections[0].columns = [], p => hero(p).type = 'script', p => hero(p).id = p.sections[0].id, p => hero(p).responsive.phone = {}, p => hero(p).responsive.tablet = {width: 99}]) {
    const page = project.defaults('home'); mutate(page);
    assert.throws(() => serialize(page));
  }
});
test('forbidden business config, HTML and internal email never export', () => {
  for (const config of [{supplier_cost: 1}, {retail_price: '100'}, {customer: {email: 'private@example.com'}}, {script: 'alert(1)'}, {css: 'color:red'}, {heading: '<b>Raw HTML</b>'}, {copy: 'staff@volcanvacations.com'}, {href: 'javascript:alert(1)'}]) {
    const page = project.defaults('home'); hero(page).config = config;
    assert.throws(() => serialize(page));
  }
  const page = project.defaults('contact'); hero(page).config.copy = 'info@volcanvacations.com';
  assert.doesNotThrow(() => serialize(page, 'contact'));
});
test('unknown and binary media, responsive refs and non-normalized focal points fail', () => {
  for (const config of [{asset: 'unknown'}, {asset: 'data:image/png;base64,abc'}, {tablet: {asset: 'unknown'}}, {poster: 'unknown'}]) {
    const page = project.defaults('home'); hero(page).config.media = {...structuredClone(core.mediaDefaults), ...config};
    assert.throws(() => serialize(page));
  }
  const page = project.defaults('home'); hero(page).config.media = {...structuredClone(core.mediaDefaults), asset: 'vv-pacific'};
  const raw = JSON.parse(serialize(page)); hero(raw).config.media.x = 50;
  assert.throws(() => parse(JSON.stringify(raw)), /normalized/);
});
test('sections, columns and cross-column movement reuse the core history', () => {
  const original = project.defaults('home'), next = structuredClone(original);
  next.sections.push({...core.base('new-section', 10), columns: [{...core.base('new-column'), widgets: []}]});
  next.sections[0].columns.push({...core.base('second-column', 1), widgets: []});
  next.sections[0].columns.forEach(c => {c.responsive.tablet = {width: 6}; c.responsive.mobile = {width: 12};});
  const moved = core.moveElement(next, hero(next).id, 'second-column', 'desktop');
  const reordered = core.moveElement(moved, 'new-section', next.sections[0].id, 'tablet');
  assert.equal(reordered.sections[0].columns[0].widgets.length, 0);
  assert.equal(reordered.sections[0].columns[1].widgets[0].type, 'hero');
  assert.equal(core.ordered(reordered.sections, 'tablet')[0].id, 'new-section');
  const h = core.commit(core.editHistory(original), reordered);
  assert.deepEqual(core.undo(h).present, original);
  assert.deepEqual(core.redo(core.undo(h)).present, reordered);
  assert.deepEqual(parse(serialize(reordered)), reordered);
});
test('safe sections may duplicate; business application widgets remain singletons', () => {
  const page = project.defaults('home'), section = structuredClone(page.sections[0]);
  section.id = 'copy-section'; section.columns[0].id = 'copy-column'; section.columns[0].widgets[0].id = 'copy-hero'; page.sections.push(section);
  assert.doesNotThrow(() => serialize(page));
  const plan = project.defaults('plan-your-trip'), duplicate = structuredClone(plan.sections[1]);
  duplicate.id = 'copy-section'; duplicate.columns[0].id = 'copy-column'; duplicate.columns[0].widgets[0].id = 'copy-form'; plan.sections.push(duplicate);
  assert.throws(() => serialize(plan, 'plan-your-trip'), /duplicated/);
});
test('oversized layouts cannot import or export', () => {
  assert.throws(() => parse(' '.repeat(100001)), /100 KB/);
  const page = project.defaults('home');
  for (let i = 0; i < 30; i++) page.sections[0].columns[0].widgets.push({...core.base('text-' + i), type: 'text', config: {text: '🌴'.repeat(950)}});
  assert.throws(() => serialize(page), /100 KB/);
});
