/* Run against development only. Requires Playwright installed outside the apps.
 * Creates explicitly DEMO records and deactivates only those records in finally.
 * Optional local transport keeps configured Codespaces origins and real servers;
 * it does not mock inventory responses or change port visibility/authentication.
 */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const web = process.env.VV_E2E_WEB_URL || 'http://localhost:3000';
const ops = process.env.VV_E2E_OPS_URL || 'http://localhost:3001';
const api = process.env.VV_E2E_API_URL || 'http://localhost:8000';
const transport = process.env.VV_E2E_LOCAL_TRANSPORT === '1';
const output = process.env.VV_E2E_OUTPUT || '/tmp/vv-m2-review';
const stamp = Date.now();
const slug = `demo-e2e-rafting-${stamp}`;
const supplierName = `DEMO E2E Supplier ${stamp}`;
const tourName = `DEMO E2E Rafting ${stamp}`;

(async () => {
  assert.equal(process.env.VV_E2E_CONFIRM_DEMO, 'yes', 'Set VV_E2E_CONFIRM_DEMO=yes for a development database');
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const origins = new Map([[new URL(web).origin, 3000], [new URL(ops).origin, 3001], [new URL(api).origin, 8000]]);
  if (transport) await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    const port = origins.get(url.origin);
    if (!port) return route.continue();
    const response = await route.fetch({url: `http://localhost:${port}${url.pathname}${url.search}`});
    await route.fulfill({response});
  });
  const requestBase = transport ? 'http://localhost:8000' : api;
  async function read(path) {
    const response = await context.request.get(requestBase + path);
    assert.equal(response.status(), 200, await response.text());
    return response.json();
  }
  const errors = [];
  context.on('page', page => page.on('pageerror', error => errors.push(error.message)));
  let supplierId, tourId;
  const results = [];
  async function readyForScreenshot(page) {
    await page.evaluate(async () => {
      for (const image of document.images) image.loading = 'eager';
      await Promise.race([
        Promise.all([document.fonts.ready, ...Array.from(document.images).map(image => image.decode().catch(() => {}))]),
        new Promise(resolve => setTimeout(resolve, 10000)),
      ]);
    });
    assert.deepEqual(await page.evaluate(() => Array.from(document.images).filter(image => !image.complete || !image.naturalWidth).map(image => image.src)), [], 'Broken/unloaded image');
  }
  try {
    const page = await context.newPage();
    assert.equal((await page.goto(ops)).status(), 200);
    await page.getByRole('link', {name: 'Manage suppliers'}).click();
    await page.getByRole('link', {name: 'New supplier', exact: true}).click();
    await page.locator('[name="name"]').fill(supplierName);
    await page.locator('[name="contact_name"]').fill('PRIVATE E2E CONTACT');
    await page.locator('[name="email"]').fill('private-e2e@example.invalid');
    await page.locator('[name="phone"]').fill('PRIVATE E2E PHONE');
    await page.locator('[name="notes"]').fill('PRIVATE E2E NOTES');
    await page.getByRole('button', {name: 'Save supplier', exact: true}).click();
    await page.waitForURL(/\/suppliers\/\d+$/);
    supplierId = Number(new URL(page.url()).pathname.split('/').pop());
    await page.locator('[name="notes"]').fill('PRIVATE E2E NOTES UPDATED');
    await page.getByRole('button', {name: 'Save supplier', exact: true}).click();
    await page.getByText('Supplier saved.', {exact: true}).waitFor();
    assert.equal((await read(`/ops/suppliers/${supplierId}`)).notes, 'PRIVATE E2E NOTES UPDATED');
    results.push('Supplier created and edited through Operations');

    await page.goto(ops + '/tours/new');
    await page.locator('[name="name"]').fill(tourName);
    await page.locator('[name="slug"]').fill(slug);
    await page.locator('[name="supplier_id"]').selectOption(String(supplierId));
    await page.locator('[name="category"]').fill('Adventure');
    await page.locator('[name="location"]').fill('Arenal — development sample');
    await page.locator('[name="duration"]').fill('Half day');
    await page.locator('[name="short_description"]').fill('Development acceptance-test experience. Not a production offer.');
    await page.locator('textarea[name="description"]').fill('Demo data created by the Milestone 2 browser acceptance test.');
    await page.locator('[name="retail_price"]').fill('85.00');
    await page.locator('[name="supplier_cost"]').fill('50.00');
    assert.equal(await page.getByLabel('Gross margin', {exact: true}).textContent(), '$35.00');
    await page.getByRole('button', {name: 'Save tour', exact: true}).click();
    await page.waitForURL(/\/tours\/\d+$/);
    tourId = Number(new URL(page.url()).pathname.split('/').pop());
    await page.getByRole('heading', {name: 'Images', exact: true}).waitFor();
    assert.equal((await read(`/ops/tours/${tourId}`)).gross_margin, '35.00');
    assert.equal((await context.request.get(`${requestBase}/public/tours/${slug}`)).status(), 404);
    results.push('Tour created, supplier assigned, Decimal prices and $35.00 margin verified; inactive detail hidden');

    const add = page.getByRole('form', {name: 'Add image', exact: true});
    async function addImage(url, alt, order, primary) {
      await add.locator('[name="image_url"]').fill(url);
      await add.locator('[name="alt_text"]').fill(alt);
      await add.locator('[name="sort_order"]').fill(String(order));
      await add.locator('[name="is_primary"]').setChecked(primary);
      await add.getByRole('button', {name: 'Add image', exact: true}).click();
      await page.getByText('Gallery saved.', {exact: true}).waitFor();
      await add.getByRole('button', {name: 'Add image', exact: true}).waitFor({state: 'visible'});
    }
    await addImage('/images/rafting.webp', 'Demo E2E primary rafting', 20, true);
    await page.getByRole('form', {name: /^Edit image/}).first().waitFor();
    await addImage('/images/waterfall.webp', 'Demo E2E waterfall gallery', 10, false);
    await page.waitForFunction(() => document.querySelectorAll('.ops-image-editor').length === 2);
    let images = await read(`/ops/tours/${tourId}/images`);
    assert.deepEqual(images.map(image => image.sort_order), [10, 20]);
    const waterfallId = images[0].id;
    const editImage = page.getByRole('form', {name: `Edit image ${waterfallId}`, exact: true});
    await editImage.locator('[name="sort_order"]').fill('0');
    await editImage.locator('[name="is_primary"]').check();
    await editImage.getByRole('button', {name: 'Save image', exact: true}).click();
    await page.getByText('Gallery saved.', {exact: true}).waitFor();
    images = await read(`/ops/tours/${tourId}/images`);
    assert.equal(images[0].sort_order, 0);
    assert.equal(images[0].is_primary, true);
    assert.equal(images.filter(image => image.is_primary).length, 1);
    results.push('Primary image, second gallery image, reordering, and primary switching verified through Operations');

    await page.locator('[name="active"]').check();
    await page.locator('[name="featured"]').check();
    await page.locator('[name="name"]').fill(tourName + ' Updated');
    await page.getByRole('button', {name: 'Save tour', exact: true}).click();
    await page.getByText('Tour saved. Server gross margin: $35.00 USD.', {exact: true}).waitFor();
    await readyForScreenshot(page);
    await page.screenshot({path: `${output}/operations-tour.png`, fullPage: true});
    const detail = await read(`/public/tours/${slug}`);
    assert.equal(detail.name, tourName + ' Updated');
    assert.equal(detail.primary_image.id, waterfallId);
    assert.equal(detail.retail_price, '85.00');
    for (const data of [detail, await read('/public/tours'), await read('/public/tours?featured=true')]) {
      const json = JSON.stringify(data);
      for (const privateField of ['supplier_cost', 'gross_margin', 'supplier_id', 'contact_name', 'email', 'phone', 'notes', 'PRIVATE E2E']) assert.ok(!json.includes(privateField), privateField);
    }
    for (const path of ['/', '/tours']) {
      const publicPage = await context.newPage();
      assert.equal((await publicPage.goto(web + path)).status(), 200);
      const card = publicPage.locator('.tour-card').filter({hasText: tourName + ' Updated'});
      await card.waitFor();
      assert.ok((await card.textContent()).includes('$85'));
      assert.equal(await card.locator('img').getAttribute('src'), '/images/waterfall.webp');
      assert.equal(await publicPage.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await readyForScreenshot(publicPage);
      await publicPage.screenshot({path: `${output}/${path === '/' ? 'homepage' : 'tours'}-published.png`, fullPage: true});
      await publicPage.close();
    }
    results.push('Operations → API → PostgreSQL → homepage and /tours PASS; public detail/gallery and sensitive-data exclusion PASS');

    page.once('dialog', dialog => dialog.accept());
    await editImage.getByRole('button', {name: 'Remove image', exact: true}).click();
    await page.waitForFunction(() => document.querySelectorAll('.ops-image-editor').length === 1);
    images = await read(`/ops/tours/${tourId}/images`);
    assert.equal(images[0].is_primary, true);
    results.push('Image removal and automatic primary promotion verified through Operations');

    for (const width of [390, 1440]) {
      for (const [origin, paths] of [[web, ['/', '/tours', '/plan-your-trip', '/about', '/contact']], [ops, ['/', '/tours', '/suppliers', '/tours/new', '/suppliers/new', `/tours/${tourId}`, `/suppliers/${supplierId}`]]]) {
        for (const path of paths) {
          const check = await context.newPage();
          await check.setViewportSize({width, height: 1000});
          assert.equal((await check.goto(origin + path)).status(), 200);
          if (origin === web && ['/', '/tours'].includes(path)) await check.locator('.tour-card').first().waitFor();
          if (origin === ops && path !== '/') {
            await check.waitForFunction(() => !document.body.innerText.includes('Loading inventory') && !document.body.innerText.includes('Loading gallery'));
          }
          assert.equal(await check.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `${origin}${path} at ${width}`);
          if (width === 390 && ['/', '/tours'].includes(path)) {
            await readyForScreenshot(check);
            await check.screenshot({path: `${output}/${origin === ops ? 'ops' : 'web'}-${path === '/' ? 'home' : 'tours'}-390.png`, fullPage: true});
          }
          await check.close();
        }
      }
    }
    results.push('All five public routes and seven Operations routes HTTP 200, no page overflow at desktop/mobile');

    // Failure/empty states are deliberately simulated separately from real E2E.
    for (const state of ['unavailable', 'empty']) {
      const check = await context.newPage();
      await check.route(`${api}/public/tours*`, route => state === 'empty'
        ? route.fulfill({status: 200, contentType: 'application/json', body: '[]', headers: {'Access-Control-Allow-Origin': web, 'Access-Control-Allow-Credentials': 'true'}})
        : route.abort());
      await check.goto(web + '/tours');
      await check.getByText(state === 'empty' ? 'No experiences are currently published for this selection.' : 'Experiences are temporarily unavailable.', {exact: false}).waitFor();
      assert.equal(await check.locator('.tour-card').count(), 0);
      await check.close();
    }
    results.push('Simulated unavailable/empty API states render safely without hardcoded inventory fallback');
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({results, supplierId, tourId, slug, transport, screenshots: output}, null, 2));
  } finally {
    // Keep test audit data recoverable, but never leave it published.
    if (tourId) {
      const tour = await read(`/ops/tours/${tourId}`);
      const keys = ['supplier_id', 'name', 'slug', 'short_description', 'description', 'product_type', 'category', 'duration', 'retail_price', 'supplier_cost', 'active', 'featured', 'location', 'minimum_age', 'difficulty'];
      const payload = Object.fromEntries(keys.map(key => [key, tour[key]]));
      const response = await context.request.put(`${requestBase}/ops/tours/${tourId}`, {data: {...payload, active: false, featured: false}});
      assert.equal(response.status(), 200);
      assert.equal((await context.request.get(`${requestBase}/public/tours/${slug}`)).status(), 404);
    }
    if (supplierId) {
      const supplier = await read(`/ops/suppliers/${supplierId}`);
      const keys = ['name', 'supplier_type', 'contact_name', 'email', 'phone', 'website', 'notes', 'active'];
      const payload = Object.fromEntries(keys.map(key => [key, supplier[key]]));
      assert.equal((await context.request.put(`${requestBase}/ops/suppliers/${supplierId}`, {data: {...payload, active: false}})).status(), 200);
    }
    console.log('Acceptance-test records deactivated; no records or source image files deleted.');
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
