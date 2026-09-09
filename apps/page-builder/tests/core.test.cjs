const {test} = require('node:test');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
test('reusable page builder core regression suite', () => {
  const env = {...process.env, NODE_PATH: path.resolve(__dirname, '../node_modules')};
  delete env.NODE_TEST_CONTEXT;
  const output = execFileSync(process.execPath, ['--test', path.resolve(__dirname, '../../..', 'packages/page-builder/tests/core.test.cjs')], {env, encoding: 'utf8'});
  require('node:assert/strict').match(output, /# pass 22/);
});
