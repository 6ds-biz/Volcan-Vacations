/* Explicit development acceptance test; real UI/API/PostgreSQL, no mocked booking data. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const web = process.env.VV_E2E_WEB_URL || 'http://localhost:3000';
const ops = process.env.VV_E2E_OPS_URL || 'http://localhost:3001';
const api = process.env.VV_E2E_API_URL || 'http://localhost:8000';
const local = process.env.VV_E2E_LOCAL_TRANSPORT === '1';
const output = process.env.VV_E2E_OUTPUT || '/tmp/vv-m3-review';
const stamp = Date.now();
const tourName = `DEMO M3 Rafting ${stamp}`;
const slug = `demo-m3-rafting-${stamp}`;
const dateAfter = days => new Date(Date.now() + days * 86400000).toISOString().slice(0, 10);

(async () => {
  assert.equal(process.env.VV_E2E_CONFIRM_DEMO, 'yes');
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const ports = new Map([[new URL(web).origin, 3000], [new URL(ops).origin, 3001], [new URL(api).origin, 8000]]);
  if (local) await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    const port = ports.get(url.origin);
    if (!port) return route.continue();
    const response = await route.fetch({url: `http://localhost:${port}${url.pathname}${url.search}`});
    await route.fulfill({response});
  });
  const direct = local ? 'http://localhost:8000' : api;
  async function request(path, method = 'GET', data) {
    const response = await context.request.fetch(direct + path, {method, data});
    assert.ok(response.ok(), `${method} ${path}: ${await response.text()}`);
    return response.status() === 204 ? null : response.json();
  }
  async function screenshot(page, name) {
    await page.evaluate(async () => {
      for (const image of document.images) image.loading = 'eager';
      await Promise.race([Promise.all([document.fonts.ready, ...Array.from(document.images).map(image => image.decode().catch(() => {}))]), new Promise(resolve => setTimeout(resolve, 10000))]);
    });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({path: `${output}/${name}.png`, fullPage: true});
  }
  const results = [];
  const step = message => { results.push(message); console.log('PASS: ' + message); };
  const errors = [];
  context.on('page', page => page.on('pageerror', error => errors.push(error.message)));
  let supplier, tour, booking;
  const supplierPayload = {name: `DEMO M3 Supplier ${stamp}`, supplier_type: 'tour_operator', notes: 'PRIVATE M3 SUPPLIER NOTE', email: 'private-m3@example.invalid', active: true};
  let tourPayload;
  try {
    supplier = await request('/ops/suppliers', 'POST', supplierPayload);
    tourPayload = {supplier_id: supplier.id, name: tourName, slug, short_description: 'DEVELOPMENT acceptance test only.', description: 'Not a real supplier offer.', category: 'Adventure', duration: 'Half day', retail_price: '85.00', supplier_cost: '50.00', active: true, featured: true};
    tour = await request('/ops/tours', 'POST', tourPayload);
    await request(`/ops/tours/${tour.id}/images`, 'POST', {image_url: '/images/rafting.webp', alt_text: 'Demo rafting', sort_order: 0, is_primary: true});
    const page = await context.newPage();
    const submissions = [];
    page.on('request', req => { if (req.method() === 'POST' && req.url().endsWith('/public/booking-requests')) submissions.push(req.postDataJSON()); });
    assert.equal((await page.goto(web + '/tours')).status(), 200);
    const card = page.locator('.tour-card').filter({hasText: tourName});
    await card.getByRole('link', {name: 'Request This Tour', exact: true}).click();
    await page.waitForURL(url => url.pathname === '/request' && url.searchParams.get('tour') === slug);
    await page.getByRole('heading', {name: tourName, exact: true}).waitFor();
    await screenshot(page, 'request-desktop');
    step('Tours CTA opens the selected experience without reselection');
    await page.setViewportSize({width: 390, height: 1000});
    await page.getByRole('button', {name: 'Send booking request', exact: true}).click();
    assert.equal(submissions.length, 0);
    await page.locator('[name="requested_date"]').fill(dateAfter(30));
    await page.locator('[name="requested_time"]').fill('09:30');
    await page.locator('[name="first_name"]').fill('DEMO Public');
    await page.locator('[name="last_name"]').fill('Traveler');
    await page.locator('[name="email"]').fill(`DEMO-M3-${stamp}@example.invalid`);
    await page.locator('[name="phone"]').fill('555-0100');
    await page.locator('[name="party_size"]').fill('2');
    await page.locator('[name="traveler_0_first_name"]').fill('DEMO Public');
    await page.locator('[name="traveler_0_last_name"]').fill('Traveler');
    await page.locator('[name="traveler_0_type"]').selectOption('adult');
    await page.getByRole('button', {name: 'Add traveler', exact: true}).click();
    await page.locator('[name="traveler_1_first_name"]').fill('DEMO Junior');
    await page.locator('[name="traveler_1_last_name"]').fill('Traveler');
    await page.locator('[name="traveler_1_type"]').selectOption('child');
    await page.locator('[name="traveler_1_dob"]').fill('2016-04-12');
    await page.locator('[name="start_date"]').fill(dateAfter(29));
    await page.locator('[name="end_date"]').fill(dateAfter(31));
    await page.locator('[name="customer_notes"]').fill('DEMO M3 request: please discuss accessibility before confirming.');
    await screenshot(page, 'request-mobile-filled');
    const responsePromise = page.waitForResponse(response => response.url().endsWith('/public/booking-requests') && response.request().method() === 'POST');
    await page.getByRole('button', {name: 'Send booking request', exact: true}).click();
    const response = await responsePromise;
    assert.equal(response.status(), 201, await response.text());
    const receipt = await response.json();
    await page.getByRole('heading', {name: 'Request Received', exact: true}).waitFor();
    assert.equal(await page.getByTestId('request-reference').textContent(), receipt.reference);
    assert.match(receipt.reference, /^VV-\d{6}-[A-F0-9]{12}$/);
    assert.equal(receipt.party_size, 2);
    assert.equal(receipt.status, 'new');
    assert.equal(submissions.length, 1);
    assert.equal(await page.getByRole('button', {name: /pay|checkout|deposit/i}).count(), 0);
    await screenshot(page, 'request-success-mobile');
    step('Mobile form validates, accepts two travelers and dates, and returns a VV receipt without payment');
    // Confirm concurrent retries return the same own receipt, not new rows.
    const parallelReceipts = await Promise.all(Array.from({length: 4}, () => request('/public/booking-requests', 'POST', submissions[0])));
    for (const replay of parallelReceipts) assert.deepEqual(replay, receipt);
    const duplicate = await request('/public/booking-requests', 'POST', submissions[0]);
    assert.deepEqual(duplicate, receipt);
    const bookings = await request('/ops/bookings');
    const matches = bookings.filter(row => row.reference === receipt.reference);
    assert.equal(matches.length, 1);
    booking = matches[0];
    assert.equal(booking.travelers.length, 2);
    assert.equal(booking.trip.party_size, 2);
    assert.equal(booking.trip.status, 'inquiry');
    assert.equal(booking.unit_price, '85.00');
    assert.equal(booking.supplier_unit_cost, '50.00');
    assert.equal(booking.gross_margin, '70.00');
    assert.equal(booking.retail_total, '170.00');
    assert.equal(booking.customer.email, `demo-m3-${stamp}@example.invalid`);
    assert.equal(booking.travelers[1].date_of_birth, '2016-04-12');
    assert.equal(booking.trip.start_date, dateAfter(29));
    tourPayload = {...tourPayload, retail_price: '99.00', supplier_cost: '60.00'};
    await request(`/ops/tours/${tour.id}`, 'PUT', tourPayload);
    const snapshot = await request(`/ops/bookings/${booking.id}`);
    assert.equal(snapshot.unit_price, '85.00');
    assert.equal(snapshot.supplier_unit_cost, '50.00');
    assert.equal(snapshot.gross_margin, '70.00');
    step('Real persisted customer/travelers/trip/reservation, idempotent replay, and immutable price/cost snapshots verified');
    const admin = await context.newPage();
    await admin.goto(ops);
    await admin.getByRole('navigation', {name: 'Operations navigation'}).getByRole('link', {name: 'Bookings', exact: true}).click();
    await admin.getByRole('link', {name: receipt.reference, exact: true}).click();
    await admin.getByRole('heading', {name: receipt.reference, exact: true}).waitFor();
    assert.ok((await admin.locator('body').textContent()).includes('DEMO Junior Traveler'));
    assert.ok((await admin.locator('body').textContent()).includes('$50.00 USD'));
    assert.ok((await admin.locator('body').textContent()).includes('$70.00 USD'));
    await admin.locator('[name="status"]').selectOption('contacted');
    const privateNote = `PRIVATE M3 FOLLOW-UP ${stamp}`;
    await admin.locator('[name="internal_notes"]').fill(privateNote);
    await admin.getByRole('button', {name: 'Save follow-up', exact: true}).click();
    await admin.getByText('Follow-up saved.', {exact: true}).waitFor();
    await admin.reload({waitUntil: 'domcontentloaded'});
    await admin.locator('[name="internal_notes"]').waitFor();
    assert.equal(await admin.locator('[name="internal_notes"]').inputValue(), privateNote);
    assert.equal(await admin.locator('[name="status"]').inputValue(), 'contacted');
    await screenshot(admin, 'operations-booking-desktop');
    await admin.setViewportSize({width: 390, height: 1000});
    await screenshot(admin, 'operations-booking-mobile');
    await admin.goto(ops + '/bookings');
    await admin.getByLabel('Filter by status').selectOption('contacted');
    await admin.getByRole('link', {name: receipt.reference, exact: true}).waitFor();
    await screenshot(admin, 'operations-inbox-mobile');
    step('Operations inbox/filter/detail, Contacted transition, and internal note persist after refresh');
    for (const data of [receipt, await request('/public/booking-requests', 'POST', submissions[0]), await request('/public/tours')]) {
      for (const field of ['supplier_cost', 'supplier_unit_cost', 'gross_margin', 'internal_notes', 'PRIVATE M3', 'contact_snapshot']) assert.ok(!JSON.stringify(data).includes(field));
    }
    for (const path of ['/public/customers', `/public/bookings/${booking.id}`, `/public/booking-requests/${receipt.reference}`]) {
      assert.equal((await context.request.get(direct + path)).status(), 404);
    }
    for (const width of [390, 1440]) {
      for (const path of ['/', '/tours', '/plan-your-trip', '/about', '/contact', `/request?tour=${slug}`]) {
        const check = await context.newPage();
        await check.setViewportSize({width, height: 1000});
        assert.equal((await check.goto(web + path)).status(), 200);
        if (path === '/' || path === '/tours') {
          const selected = check.locator('.tour-card').filter({hasText: tourName});
          await selected.waitFor();
          assert.equal(await selected.getByRole('link', {name: 'Request This Tour', exact: true}).getAttribute('href'), `/request?tour=${slug}`);
        }
        assert.equal(await check.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        await check.close();
      }
    }
    assert.deepEqual(errors, []);
    step('Homepage CTA, all six public routes, desktop/mobile layout, and public privacy boundary verified');
    console.log(JSON.stringify({results, reference: receipt.reference, bookingId: booking.id, customerId: booking.customer.id, tripId: booking.trip.id, localTransport: local, screenshots: output}, null, 2));
  } finally {
    if (booking) {
      const current = await request(`/ops/bookings/${booking.id}`);
      await request(`/ops/bookings/${booking.id}`, 'PUT', {status: 'cancelled', expected_status: current.status, internal_notes: `${current.internal_notes || ''}\nDEMO acceptance test completed; cancelled for cleanup.`, trip_status: 'cancelled'});
    }
    if (tour) await request(`/ops/tours/${tour.id}`, 'PUT', {...tourPayload, active: false, featured: false});
    if (supplier) await request(`/ops/suppliers/${supplier.id}`, 'PUT', {...supplierPayload, active: false});
    await browser.close();
    console.log('Only test-owned booking/trip cancelled and test-owned inventory deactivated. Demo audit records retained; no records deleted.');
  }
})().catch(error => { console.error(error); process.exit(1); });
