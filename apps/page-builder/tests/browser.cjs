const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const base = process.env.BUILDER_URL || 'http://localhost:3002';
const output = path.resolve(__dirname, '../test-results');

(async () => {
  await fs.mkdir(output, {recursive: true});
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}, hasTouch: true});
  const page = await context.newPage(), errors = [], requests = [], results = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {if (/\/api\/|\/public\/tours|paypal|:8000|:3000|:3001/.test(request.url())) requests.push(request.url());});
  page.setDefaultTimeout(15000);
  const button = name => page.getByRole('button', {name, exact: true});
  const frame = () => page.frameLocator('iframe');
  const structure = async () => page.getByRole('tab', {name: 'Structure', exact: true}).click();
  async function selectWidget(section = 0, widget = 0) {
    await structure();
    await page.locator('.pb-tree > li').nth(section).locator('ul ul button').nth(widget).click();
  }
  async function exported() {
    const pending = page.waitForEvent('download'); await button('Export').click();
    const download = await pending; const data = await fs.readFile(await download.path(), 'utf8');
    return {data, name: download.suggestedFilename(), value: JSON.parse(data)};
  }
  async function importRaw(data, accept = true) {
    if (!await page.getByLabel('Import layout JSON', {exact: true}).count()) await button('Import').click();
    await page.getByLabel('Import layout JSON', {exact: true}).fill(data);
    page.once('dialog', dialog => accept ? dialog.accept() : dialog.dismiss());
    await button('Import layout').click();
  }
  try {
    await page.goto(base, {timeout: 90000});
    await page.locator('.pb-editor').waitFor();
    await frame().locator('.home-hero h1').waitFor();
    assert.equal(await page.getByLabel('Project', {exact: true}).inputValue(), 'volcan-vacations');
    const headings = ['home', 'tours', 'tour-detail', 'plan-your-trip', 'about', 'contact'];
    for (const key of headings) {
      await page.getByLabel('Page', {exact: true}).selectOption(key);
      await frame().locator('main').waitFor();
      await structure();
      assert(await page.locator('.pb-tree > li').count() >= 2);
      const data = await exported(); assert.equal(data.value.page_type, key);
      assert(!/retail_price|supplier_cost|credentials|customer_data|base64/.test(data.data));
      for (const device of ['Desktop', 'Tablet', 'Mobile']) {
        await button(device).click(); await button('Preview').click();
        assert.equal(await page.locator('.pb-editor-panel').count(), 0);
        assert.equal(await frame().locator('.pb-node-bar').count(), 0);
        assert.equal(await page.locator('iframe').evaluate(node => node.contentWindow.innerWidth), {Desktop: 1440, Tablet: 900, Mobile: 390}[device]);
        await page.screenshot({path: path.join(output, `preview-${key}-${device.toLowerCase()}.png`)});
        await button('Back to editor').click();
      }
    }
    results.push('All six defaults, 18 clean device previews, project exports');
    await page.getByLabel('Page', {exact: true}).selectOption('home'); await button('Desktop').click();
    await selectWidget(); await page.getByLabel('Headline', {exact: true}).fill('Your Costa Rica adventure');
    await page.getByLabel('Eyebrow', {exact: true}).fill('Discover with us');
    await page.getByLabel('Subheadline', {exact: true}).fill('At your own pace');
    await page.getByLabel('Body', {exact: true}).fill('Thoughtful experiences made for you.');
    await page.getByLabel('CTA label', {exact: true}).fill('Start planning');
    await page.getByLabel('CTA link', {exact: true}).fill('/plan-your-trip'); await page.getByLabel('Headline', {exact: true}).focus();
    await page.getByLabel('Accent', {exact: true}).selectOption('gold-light');
    await page.getByLabel('Section spacing', {exact: true}).selectOption('large');
    await button('Change Image').click();
    await page.locator('.pb-picker-grid button').filter({hasText: 'papagayo-temporary.webp'}).click();
    await page.getByLabel('Alt text', {exact: true}).fill('Illustrative Pacific cove');
    await button('Set focal point on image').click({position: {x: 60, y: 45}});
    await page.getByLabel('overlay', {exact: true}).selectOption('dark');
    await page.getByLabel('fit', {exact: true}).selectOption('contain');
    await button('Tablet').click();
    await page.locator('.pb-picker-grid button').filter({hasText: 'nosara-temporary.webp'}).click();
    await page.getByLabel('Focal x', {exact: true}).fill('67');
    await button('Mobile').click(); await page.getByLabel('Focal y', {exact: true}).fill('31');
    await button('Desktop').click();
    await page.getByLabel('Page', {exact: true}).selectOption('about');
    await page.getByLabel('Page', {exact: true}).selectOption('home');
    await selectWidget(); assert.equal(await page.getByLabel('Headline', {exact: true}).inputValue(), 'Your Costa Rica adventure');
    await page.getByLabel('Headline', {exact: true}).fill('Undo this edit'); await button('Undo').click();
    assert.equal(await page.getByLabel('Headline', {exact: true}).inputValue(), 'Your Costa Rica adventure');
    await button('Redo').click(); assert.equal(await page.getByLabel('Headline', {exact: true}).inputValue(), 'Undo this edit'); await button('Undo').click();
    const edited = await exported(), media = edited.value.sections[0].columns[0].widgets[0].config.media;
    assert.equal(edited.name, 'vv-home-layout.json'); assert.equal(media.asset, 'vv-papagayo');
    assert.equal(media.tablet.asset, 'vv-nosara'); assert.equal(media.tablet.x, .67); assert.equal(media.mobile.y, .31);
    assert(media.x >= 0 && media.x <= 1); assert.equal(media.fit, 'contain');
    await importRaw(edited.data); assert.equal((await exported()).data, edited.data);
    await importRaw('{"schema_version":99}'); await page.getByRole('alert').filter({hasText: 'configuration'}).waitFor();
    assert.equal((await exported()).data, edited.data);
    await page.getByLabel('Import Layout JSON file', {exact: true}).setInputFiles({name: edited.name, mimeType: 'application/json', buffer: Buffer.from(edited.data)});
    await button('Import layout').click(); assert.equal((await exported()).data, edited.data);
    await button('Import').click();
    await selectWidget(); await button('Change Image').click();
    await button('Reset media to default').click();
    assert.equal((await exported()).value.sections[0].columns[0].widgets[0].config.media, undefined);
    await button('Undo').click(); assert.equal((await exported()).data, edited.data);
    await page.getByLabel('Decorative', {exact: true}).selectOption('true');
    assert.equal((await exported()).value.sections[0].columns[0].widgets[0].config.media.decorative, true);
    await button('Undo').click();
    results.push('Structured text, tokens, approved media, visual focal point, responsive media, retained pages, undo/redo, file import, invalid import, deterministic round trip');
    await structure(); await button('Add section').click(); await button('Add column').click();
    await structure(); const lastSection = page.locator('.pb-tree > li').last();
    await lastSection.locator(':scope > ul > li > button').first().click();
    await page.getByLabel('width', {exact: true}).selectOption('6');
    await page.getByRole('tab', {name: 'Widgets', exact: true}).click(); await page.locator('aside').getByRole('button', {name: 'Heading', exact: true}).click();
    await page.getByLabel('Heading text', {exact: true}).fill('A new section');
    await button('Duplicate').click(); await button('Move Right').click();
    let layout = (await exported()).value; assert.equal(layout.sections.at(-1).columns[1].widgets.length, 1);
    await button('Move Left').click(); await button('Move Down').click(); await button('Move Up').click();
    await button('Mobile').click(); await page.getByLabel('Visibility', {exact: true}).selectOption('false');
    await page.getByLabel('width', {exact: true}).selectOption('12'); await button('Desktop').click();
    await button('Remove').click(); await button('Undo').click();
    await structure(); await page.locator('.pb-tree > li > button').last().click(); await button('Duplicate').click();
    await button('Move Up').click(); await button('Move Down').click();
    // Exercise actual pointer drag inside the scaled public canvas.
    await page.locator('.pb-editor-canvas').evaluate(node => node.scrollTop = node.scrollHeight);
    const beforeDrag = (await exported()).value;
    const dragWidgets = beforeDrag.sections.at(-1).columns[0].widgets;
    assert.equal(dragWidgets.length, 2);
    const source = frame().locator(`[data-pb-key="${dragWidgets[0].id}"] > .pb-node-bar .pb-handle`);
    const destination = frame().locator(`[data-pb-key="${dragWidgets[1].id}"] > .pb-node-bar .pb-handle`);
    await source.scrollIntoViewIfNeeded(); await destination.scrollIntoViewIfNeeded();
    const a = await source.boundingBox(), b = await destination.boundingBox();
    assert(a && b);
    await page.mouse.move(a.x + a.width / 2, a.y + a.height / 2); await page.mouse.down();
    await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, {steps: 12}); await page.mouse.up();
    layout = (await exported()).value; assert(layout.sections.length >= 12);
    const afterDrag = layout.sections.at(-1).columns[0].widgets;
    const order = widgets => [...widgets].sort((a,b) => (a.responsive.desktop?.order ?? a.presentation.order) - (b.responsive.desktop?.order ?? b.presentation.order)).map(w => w.id);
    assert.deepEqual(order(afterDrag), order(dragWidgets).reverse(), 'Pointer drag must reorder the widgets');
    results.push('Sections, duplication, columns, resizing, widget insertion/removal, precise movement, drag, responsive visibility');
    // Discard warning protects the current page; cancellation retains its design.
    await selectWidget(); await page.getByLabel('Headline', {exact: true}).fill('Keep this unsaved change');
    page.removeAllListeners('dialog'); page.once('dialog', dialog => dialog.dismiss()); await button('New from VV Default').click();
    assert.equal(await page.getByLabel('Headline', {exact: true}).inputValue(), 'Keep this unsaved change');
    page.once('dialog', dialog => dialog.accept()); await button('New from VV Default').click();
    for (const width of [1440, 1024, 768]) {
      await page.setViewportSize({width, height: 1000}); await button('Desktop').click();
      await frame().locator('.home-hero h1').waitFor();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), width);
      const panel = await page.locator('.pb-editor-panel').boundingBox(), canvas = await page.locator('.pb-editor-canvas').boundingBox();
      assert(canvas.width > panel.width); assert(panel.height > 400);
      assert((await button('Import').boundingBox()).height >= 44);
      await page.screenshot({path: path.join(output, `builder-${width}.png`)});
      await page.getByRole('tab', {name: 'Widgets', exact: true}).tap();
      await structure();
    }
    assert.equal(await page.evaluate(() => localStorage.length), 0);
    assert.deepEqual(requests, []); assert.deepEqual(errors, []);
    results.push('Discard warning; 1440/1024/768 touch layouts; zero API/payment requests, browser storage, or runtime errors');
    await fs.writeFile(path.join(output, 'results.json'), JSON.stringify({results, errors, requests}, null, 2));
    console.log(JSON.stringify({results, errors, requests}, null, 2));
  } catch (error) {
    await page.screenshot({path: path.join(output, 'failure.png')}).catch(() => {});
    console.error(error); console.error({errors, requests, results}); process.exitCode = 1;
  } finally { await browser.close(); }
})();
