/* Explicit development acceptance: real public UI, Operations, API and PostgreSQL. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {randomUUID} = require('node:crypto');
const web = process.env.VV_E2E_WEB_URL || 'http://localhost:3000';
const ops = process.env.VV_E2E_OPS_URL || 'http://localhost:3001';
const api = process.env.VV_E2E_API_URL || 'http://localhost:8000';
const local = process.env.VV_E2E_LOCAL_TRANSPORT === '1';
const output = process.env.VV_E2E_OUTPUT || '/tmp/vv-m4-review';
const stamp = Date.now();
const dateAfter = days => new Date(Date.now() + days * 86400000).toISOString().slice(0, 10);

(async () => {
  assert.equal(process.env.VV_E2E_CONFIRM_DEMO, 'yes', 'Explicit development demo opt-in required');
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  if (local) {
    const ports = new Map([[new URL(web).origin, 3000], [new URL(ops).origin, 3001], [new URL(api).origin, 8000]]);
    await context.route('**/*', async route => {
      const url = new URL(route.request().url());
      const port = ports.get(url.origin);
      if (!port) return route.continue();
      const response = await route.fetch({url: `http://localhost:${port}${url.pathname}${url.search}`});
      await route.fulfill({response});
    });
  }
  const direct = local ? 'http://localhost:8000' : api;
  async function request(path, method = 'GET', data) {
    const response = await context.request.fetch(direct + path, {method, data});
    assert.ok(response.ok(), `${method} ${path}: ${await response.text()}`);
    return response.status() === 204 ? null : response.json();
  }
  const results = [];
  const step = value => {results.push(value); console.log('PASS: ' + value);};
  const errors = [];
  context.on('page', page => page.on('pageerror', error => errors.push(error.message)));
  async function screenshot(page, name) {
    await page.evaluate(async () => {
      for (const image of document.images) image.loading = 'eager';
      await Promise.race([Promise.all([document.fonts.ready, ...Array.from(document.images).map(image => image.decode().catch(() => {}))]), new Promise(resolve => setTimeout(resolve, 10000))]);
    });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({path: `${output}/${name}.png`, fullPage: true});
  }
  let supplier, tour;
  const bookings = [];
  const submissions = [];
  const receipts = [];
  const supplierPayload = {name: `DEMO M4 Supplier ${stamp}`, supplier_type: 'tour_operator', contact_name: 'PRIVATE SUPPLIER PERSON', phone: 'PRIVATE PHONE 555', email: 'private-m4@example.invalid', notes: 'PRIVATE M4 SUPPLIER NOTES', active: true};
  let tourPayload;
  try {
    supplier = await request('/ops/suppliers', 'POST', supplierPayload);
    tourPayload = {supplier_id: supplier.id, name: `DEMO M4 Rafting ${stamp}`, slug: `demo-m4-rafting-${stamp}`, short_description: 'DEVELOPMENT acceptance only.', description: 'No real supplier offer or communication.', category: 'Adventure', duration: 'Half day', retail_price: '85.00', supplier_cost: '50.00', active: true, featured: true};
    tour = await request('/ops/tours', 'POST', tourPayload);
    await request(`/ops/tours/${tour.id}/images`, 'POST', {image_url: '/images/rafting.webp', alt_text: 'Demo rafting', sort_order: 0, is_primary: true});
    async function publicRequest(suffix, days) {
      const page = await context.newPage();
      await page.setViewportSize({width: 390, height: 1000});
      await page.goto(web + '/tours');
      await page.locator('.tour-card').filter({hasText: tour.name}).getByRole('link', {name: 'Request This Tour', exact: true}).click();
      await page.waitForURL(url => url.pathname === '/request' && url.searchParams.get('tour') === tour.slug);
      await page.getByRole('heading', {name: tour.name, exact: true}).waitFor();
      await page.locator('[name="requested_date"]').fill(dateAfter(days));
      await page.locator('[name="requested_time"]').fill('09:30');
      await page.locator('[name="first_name"]').fill('DEMO M4');
      await page.locator('[name="last_name"]').fill(suffix);
      await page.locator('[name="email"]').fill(`demo-m4-${stamp}-${suffix.toLowerCase()}@example.invalid`);
      await page.locator('[name="party_size"]').fill('1');
      await page.locator('[name="traveler_0_first_name"]').fill('DEMO M4');
      await page.locator('[name="traveler_0_last_name"]').fill(suffix);
      await page.locator('[name="traveler_0_type"]').selectOption('adult');
      const responsePromise = page.waitForResponse(r => r.url().endsWith('/public/booking-requests') && r.request().method() === 'POST');
      await page.getByRole('button', {name: 'Send booking request', exact: true}).click();
      const response = await responsePromise;
      assert.equal(response.status(), 201, await response.text());
      submissions.push(response.request().postDataJSON());
      const receipt = await response.json(); receipts.push(receipt);
      await page.getByRole('heading', {name: 'Request Received', exact: true}).waitFor();
      assert.equal(await page.getByTestId('request-reference').textContent(), receipt.reference);
      const row = (await request('/ops/bookings')).find(b => b.reference === receipt.reference);
      assert.ok(row); bookings.push(row);
      assert.equal(row.availability_status, 'unknown');
      assert.equal(row.supplier_confirmation_status, 'not_requested');
      assert.equal(row.product_availability, null);
      assert.equal(row.ready_for_payment, false);
      await screenshot(page, `public-request-${suffix.toLowerCase()}`);
      await page.close();
      return row;
    }
    const positive = await publicRequest('Confirmed', 30);
    const admin = await context.newPage();
    await admin.goto(ops + '/bookings');
    await admin.getByRole('link', {name: positive.reference, exact: true}).click();
    await admin.getByRole('heading', {name: positive.reference, exact: true}).waitFor();
    assert.match(await admin.getByTestId('confirmation-state').textContent(), /Reservation availability: Unknown/);
    async function action(kind, fields = {}) {
      await admin.locator('[name="event_type"]').selectOption(kind);
      for (const [name, value] of Object.entries(fields)) {
        const input = admin.locator(`[name="${name}"]`);
        if (await input.evaluate(el => el.tagName) === 'SELECT') await input.selectOption(value);
        else await input.fill(value);
      }
      const pending = admin.waitForResponse(r => /\/supplier-events$/.test(r.url()) && r.request().method() === 'POST');
      await admin.getByRole('button', {name: 'Record action', exact: true}).click();
      const response = await pending;
      assert.equal(response.status(), 200, await response.text());
      const row = await response.json();
      await admin.getByRole('heading', {name: row.reference, exact: true}).waitFor();
      await admin.locator('.ops-timeline li').nth(row.supplier_events.length - 1).waitFor();
      return row;
    }
    let row = await action('contacted', {contact_method: 'whatsapp', operator_identifier: 'DEMO acceptance operator', notes: 'PRIVATE M4 CONTACT — manual record only'});
    assert.equal(row.status, 'pending_supplier'); assert.equal(row.supplier_confirmation_status, 'awaiting_supplier');
    assert.match(await admin.locator('.ops-timeline').textContent(), /WhatsApp/);
    assert.match(await admin.getByTestId('confirmation-state').textContent(), /Awaiting supplier/);
    step('Public mobile request appears in Operations as Unknown; WhatsApp contact records Awaiting Supplier and a timeline event');
    const dates = await context.newPage();
    await dates.goto(ops + `/tours/${tour.id}`);
    await dates.getByRole('link', {name: 'Manage tour availability', exact: true}).click();
    await dates.getByLabel('Filter by tour').selectOption(String(tour.id));
    await dates.getByRole('button', {name: 'Add date', exact: true}).click();
    await dates.locator('[name="product_id"]').selectOption(String(tour.id));
    await dates.locator('[name="date"]').fill(positive.requested_date);
    await dates.locator('[name="status"]').selectOption('available');
    await dates.locator('[name="source"]').selectOption('supplier');
    await dates.locator('[name="notes"]').fill('PRIVATE M4 CHECK — available, capacity not provided');
    const savedDate = dates.waitForResponse(r => r.url().endsWith('/ops/availability') && r.request().method() === 'POST');
    await dates.getByRole('button', {name: 'Save availability', exact: true}).click();
    assert.equal((await savedDate).status(), 201);
    await dates.getByRole('button', {name: `Edit ${tour.name} ${positive.requested_date}`, exact: true}).waitFor();
    const editDate = async (checkedAt, note) => {
      await dates.getByRole('button', {name: `Edit ${tour.name} ${positive.requested_date}`, exact: true}).click();
      const checked = new Date(checkedAt);
      const localTime = new Date(checked.getTime() - checked.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      await dates.locator('[name="last_checked_at"]').fill(localTime);
      await dates.locator('[name="notes"]').fill(note);
      const pending = dates.waitForResponse(r => /\/ops\/availability\/\d+$/.test(r.url()) && r.request().method() === 'PUT');
      await dates.getByRole('button', {name: 'Save availability', exact: true}).click();
      const response = await pending;
      assert.equal(response.status(), 200, await response.text());
      await dates.getByRole('button', {name: `Edit ${tour.name} ${positive.requested_date}`, exact: true}).waitFor();
      return response.json();
    };
    const stale = await editDate(Date.now() - 48 * 3600000, 'PRIVATE M4 old check');
    assert.equal(stale.stale, true);
    await dates.getByText('Availability may be stale', {exact: true}).waitFor();
    assert.equal((await request(`/public/tours/${tour.slug}/availability?date=${positive.requested_date}`)).status, 'unknown');
    await editDate(Date.now(), 'PRIVATE M4 fresh recheck, capacity not provided');
    step('Availability editor updates a recorded date; stale check is flagged internally and becomes Unknown publicly until rechecked');
    await screenshot(dates, 'availability-desktop');
    await dates.setViewportSize({width: 390, height: 1000});
    await screenshot(dates, 'availability-mobile');
    await admin.reload();
    await admin.getByRole('heading', {name: 'Tour / date availability', exact: true}).waitFor();
    assert.match(await admin.locator('.ops-confirmation').textContent(), /Source: Supplier/);
    row = await action('availability_checked', {availability_status: 'available', notes: 'PRIVATE M4 request availability checked'});
    assert.equal(row.status, 'pending_supplier'); assert.equal(row.ready_for_payment, false);
    assert.equal(row.product_availability.status, 'available');
    const reference = `PRIVATE-M4-REF-${stamp}`;
    row = await action('confirmed', {reference, notes: 'PRIVATE M4 supplier confirmed original request'});
    assert.equal(row.status, 'confirmed'); assert.equal(row.availability_status, 'available');
    assert.equal(row.supplier_confirmation_status, 'confirmed'); assert.equal(row.ready_for_payment, true);
    assert.equal(row.supplier_confirmation_reference, reference);
    await admin.reload();
    await admin.getByText('Ready for Payment', {exact: true}).waitFor();
    assert.match(await admin.locator('.ops-timeline').textContent(), new RegExp(reference));
    await screenshot(admin, 'supplier-confirmed-desktop');
    await admin.setViewportSize({width: 390, height: 1000});
    await screenshot(admin, 'supplier-confirmed-mobile');
    await admin.getByTestId('confirmation-state').screenshot({path: `${output}/supplier-confirmed-state-mobile.png`});
    await admin.locator('.ops-confirmation .ops-editor').screenshot({path: `${output}/supplier-action-form-mobile.png`});
    step('Tour/date availability and request availability stay separate; supplier reference persists and booking becomes Confirmed / Ready for Payment');
    // Real PostgreSQL locking: two different commands with one version cannot both win.
    const command = {command_id: randomUUID(), expected_version: row.version, event_type: 'note', occurred_at: new Date().toISOString(), notes: 'PRIVATE M4 concurrent edit test'};
    const racing = await Promise.all([command, {...command, command_id: randomUUID(), notes: 'PRIVATE M4 competing edit'}].map(data => context.request.post(direct + `/ops/bookings/${row.id}/supplier-events`, {data})));
    assert.deepEqual(racing.map(r => r.status()).sort(), [200, 409]);
    row = await request(`/ops/bookings/${row.id}`);
    const retryCommand = {...command, command_id: randomUUID(), expected_version: row.version, occurred_at: new Date().toISOString(), notes: 'PRIVATE M4 idempotent retry'};
    const retries = await Promise.all([1, 2].map(() => request(`/ops/bookings/${row.id}/supplier-events`, 'POST', retryCommand)));
    assert.deepEqual(retries[0], retries[1]);
    assert.equal(retries[0].supplier_events.length, row.supplier_events.length + 1);
    assert.equal(retries[0].supplier_confirmation_reference, reference);
    step('PostgreSQL rejects competing stale actions; simultaneous identical action retries append exactly one event');
    const negative = await publicRequest('Declined', 32);
    await admin.goto(ops + `/bookings/${negative.id}`);
    await admin.locator('[name="event_type"]').waitFor();
    row = await action('contacted', {contact_method: 'whatsapp', notes: 'PRIVATE M4 second supplier enquiry'});
    row = await action('declined', {notes: 'PRIVATE M4 departure unavailable'});
    assert.equal(row.status, 'contacted'); assert.equal(row.availability_status, 'unavailable');
    assert.equal(row.supplier_confirmation_status, 'declined'); assert.equal(row.needs_attention, true);
    assert.equal(row.trip.status, 'inquiry');
    assert.match(await admin.getByTestId('confirmation-state').textContent(), /Alternative Needed/);
    row = await action('alternative_offered', {alternative_date: dateAfter(33), alternative_time: '11:00', alternative_product_id: String(tour.id), notes: 'PRIVATE M4 ask customer about next day'});
    assert.equal(row.supplier_confirmation_status, 'alternative_offered'); assert.equal(row.ready_for_payment, false);
    for (const key of ['product_id', 'requested_date', 'requested_time', 'unit_price', 'supplier_unit_cost', 'trip']) assert.deepEqual(row[key], negative[key]);
    assert.deepEqual(row.supplier_events.map(e => e.event_type), ['contacted', 'declined', 'alternative_offered']);
    await admin.reload();
    await admin.locator('.ops-timeline li').nth(2).waitFor();
    assert.match(await admin.locator('.ops-timeline').textContent(), /Proposed alternative/);
    await screenshot(admin, 'supplier-alternative-mobile');
    await admin.setViewportSize({width: 1440, height: 1000});
    await screenshot(admin, 'supplier-alternative-desktop');
    await admin.goto(ops + '/bookings');
    await admin.getByRole('link', {name: negative.reference, exact: true}).waitFor();
    assert.equal(await admin.getByRole('link', {name: positive.reference, exact: true}).count(), 0);
    await admin.getByLabel('Needs Attention only', {exact: true}).uncheck();
    await admin.getByRole('link', {name: positive.reference, exact: true}).waitFor();
    await screenshot(admin, 'booking-inbox');
    await admin.goto(ops);
    await admin.locator('.ops-metrics dd').first().waitFor();
    await screenshot(admin, 'dashboard');
    step('Decline marks Unavailable and Needs Attention without cancelling the trip; alternative date/time and full history persist without changing original prices or request');
    for (let i = 0; i < submissions.length; i++) assert.deepEqual(await request('/public/booking-requests', 'POST', submissions[i]), receipts[i]);
    const safeDate = await request(`/public/tours/${tour.slug}/availability?date=${positive.requested_date}`);
    assert.deepEqual(safeDate, {date: positive.requested_date, status: 'available', request_required: true});
    const unknownDate = await request(`/public/tours/${tour.slug}/availability?date=${negative.requested_date}`);
    assert.equal(unknownDate.status, 'unknown'); // reservation decline never becomes shared date inventory
    for (const data of [...receipts, safeDate, unknownDate, await request('/public/tours'), await request(`/public/tours/${tour.slug}`)]) {
      for (const field of ['PRIVATE', 'supplier_cost', 'supplier_unit_cost', 'gross_margin', 'internal_notes', 'supplier_confirmation', 'supplier_events', 'remaining_capacity', 'last_checked_at', 'operator_identifier', 'private-m4@example.invalid']) assert.ok(!JSON.stringify(data).includes(field), field);
    }
    for (const path of [`/public/bookings/${positive.id}`, '/public/customers']) assert.equal((await context.request.get(direct + path)).status(), 404);
    for (const width of [1440, 900, 390]) {
      const page = await context.newPage(); await page.setViewportSize({width, height: 1000});
      for (const path of ['/', '/tours', '/plan-your-trip', '/about', '/contact', `/request?tour=${tour.slug}`]) {
        assert.equal((await page.goto(web + path)).status(), 200);
        if (path === '/') {await page.locator('.tour-card').first().waitFor(); await screenshot(page, `homepage-${width}`);}
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      }
      await page.close();
    }
    assert.deepEqual(errors, []);
    step('Public allowlists hide supplier details and keep Request This Tour; six public routes pass at 1440px, 900px and 390px');
    const report = {results, references: bookings.map(b => b.reference), bookingIds: bookings.map(b => b.id), localTransport: local, output};
    fs.writeFileSync(`${output}/e2e-results.json`, JSON.stringify(report, null, 2));
    console.log(JSON.stringify(report, null, 2));
  } catch (error) {
    for (const [index, page] of context.pages().entries()) {
      console.error('Failure page:', page.url());
      await page.screenshot({path: `${output}/failure-${index}.png`, fullPage: true}).catch(() => {});
      fs.writeFileSync(`${output}/failure-${index}.txt`, await page.locator('body').innerText().catch(() => 'Page unavailable'));
    }
    throw error;
  } finally {
    for (const booking of bookings) {
      const current = await request(`/ops/bookings/${booking.id}`);
      await request(`/ops/bookings/${booking.id}`, 'PUT', {status: 'cancelled', expected_status: current.status, expected_version: current.version, internal_notes: 'DEMO M4 acceptance completed; cancelled for cleanup. Supplier timeline retained.', trip_status: 'cancelled'});
    }
    if (tour) await request(`/ops/tours/${tour.id}`, 'PUT', {...tourPayload, active: false, featured: false});
    if (supplier) await request(`/ops/suppliers/${supplier.id}`, 'PUT', {...supplierPayload, active: false});
    await browser.close();
    console.log('Only test-owned bookings/trips cancelled and test-owned inventory deactivated. Audit records retained; no records deleted.');
  }
})().catch(error => {console.error(error); process.exit(1);});
