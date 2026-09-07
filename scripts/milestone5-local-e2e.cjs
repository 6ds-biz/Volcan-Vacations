/* Real local UI/API/DB acceptance. No provider mock, no fake capture, no sandbox-success claim. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {randomUUID} = require('node:crypto');
const web = process.env.VV_E2E_WEB_URL || 'http://localhost:3000';
const ops = process.env.VV_E2E_OPS_URL || 'http://localhost:3001';
const api = process.env.VV_E2E_API_URL || 'http://localhost:8000';
const local = process.env.VV_E2E_LOCAL_TRANSPORT === '1';
const output = process.env.VV_E2E_OUTPUT || '/tmp/vv-m5-review';
const stamp = Date.now();
(async () => {
  assert.equal(process.env.VV_E2E_CONFIRM_DEMO, 'yes');
  const browser = await chromium.launch({args: ['--no-sandbox']});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const errors = [];
  context.on('page', page => page.on('pageerror', e => errors.push(e.message)));
  fs.mkdirSync(output, {recursive: true});
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
  async function request(path, method='GET', data, headers) {
    const response = await context.request.fetch(direct + path, {method, data, headers});
    assert.ok(response.ok(), `${method} ${path}: ${await response.text()}`);
    return response.json();
  }
  async function shot(page, name) {
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({path: `${output}/${name}.png`, fullPage: true});
  }
  let supplier, tour, booking;
  const supplierBody = {name: `DEMO M5 Supplier ${stamp}`, supplier_type: 'tour_operator', notes: 'PRIVATE M5 supplier', active: true};
  let tourBody;
  try {
    supplier = await request('/ops/suppliers', 'POST', supplierBody);
    tourBody = {supplier_id: supplier.id, name: `DEMO M5 Tour ${stamp}`, slug: `demo-m5-${stamp}`, short_description: 'Development checkout validation only', description: 'No actual tour or payment', category: 'Adventure', duration: 'Half day', retail_price: '85.00', supplier_cost: '50.00', active: true, featured: false};
    tour = await request('/ops/tours', 'POST', tourBody);
    const publicPage = await context.newPage();
    await publicPage.goto(web + '/request?tour=' + tour.slug);
    await publicPage.getByRole('heading', {name: tour.name, exact: true}).waitFor();
    await publicPage.locator('[name="requested_date"]').fill(new Date(Date.now()+30*86400000).toISOString().slice(0,10));
    await publicPage.locator('[name="first_name"]').fill('DEMO M5');
    await publicPage.locator('[name="last_name"]').fill('Visitor');
    await publicPage.locator('[name="email"]').fill(`demo-m5-${stamp}@example.invalid`);
    await publicPage.locator('[name="party_size"]').fill('2');
    await publicPage.locator('[name="traveler_0_first_name"]').fill('DEMO M5');
    await publicPage.locator('[name="traveler_0_last_name"]').fill('Visitor');
    const submitted = publicPage.waitForResponse(r => r.url().endsWith('/public/booking-requests') && r.request().method() === 'POST');
    await publicPage.getByRole('button', {name: 'Send booking request', exact: true}).click();
    const response = await submitted;
    assert.equal(response.status(), 201);
    const receipt = await response.json();
    await publicPage.getByRole('heading', {name: 'Request Received', exact: true}).waitFor();
    booking = (await request('/ops/bookings')).find(b => b.reference === receipt.reference);
    assert.ok(booking);
    const refused = await context.request.post(direct + `/ops/bookings/${booking.id}/payment-link`, {data:{expected_version:booking.version}});
    assert.equal(refused.status(), 409);
    const admin = await context.newPage();
    await admin.goto(ops + `/bookings/${booking.id}`);
    await admin.getByRole('heading', {name: 'Not Ready', exact: true}).waitFor();
    await admin.locator('[name="event_type"]').selectOption('confirmed');
    await admin.locator('[name="reference"]').fill('PRIVATE M5 SUPPLIER CONFIRMATION');
    const confirmed = admin.waitForResponse(r => r.url().endsWith('/supplier-events') && r.request().method() === 'POST');
    await admin.getByRole('button', {name: 'Record action', exact: true}).click();
    assert.equal((await confirmed).status(), 200);
    await admin.getByRole('button', {name: 'Generate payment link', exact: true}).waitFor();
    await admin.getByRole('button', {name: 'Generate payment link', exact: true}).click();
    const openLink = admin.getByRole('link', {name: 'Open customer payment page', exact: true});
    await openLink.waitFor();
    const url = await openLink.getAttribute('href');
    const token = new URL(url).hash.split('token=')[1];
    assert.match(token, /^[A-Za-z0-9_-]{43}$/);
    assert.equal(new URL(url).pathname, '/pay');
    await request(`/ops/tours/${tour.id}`, 'PUT', {...tourBody, retail_price: '95.00'});
    const payment = await context.newPage();
    const paymentRequests = [];
    payment.on('request', req => {if (req.url().includes('/public/payments/')) paymentRequests.push(req);});
    await payment.goto(url);
    await payment.getByText('Your tour has been confirmed and is ready for payment.', {exact:true}).waitFor();
    assert.match(await payment.locator('.vv-payment').textContent(), /\$170.00 USD/);
    const session = await request('/public/payments/session', 'GET', undefined, {Authorization: 'Bearer ' + token});
    assert.equal(session.amount, '170.00');
    for (const field of ['supplier_cost','supplier_unit_cost','margin','internal_notes','PRIVATE','capture_id','client_secret','webhook_id']) assert.ok(!JSON.stringify(session).includes(field));
    for (const width of [1440,900,390]) {
      await payment.setViewportSize({width,height:1000});
      await shot(payment, `payment-page-${width}`);
    }
    for (const req of paymentRequests) {
      assert.ok(!req.url().includes(token));
      assert.ok(!req.url().includes('#'));
      assert.equal(req.headers().authorization, 'Bearer ' + token);
    }
    assert.equal(await payment.locator('meta[name="referrer"]').getAttribute('content'), 'no-referrer');
    assert.match(await payment.locator('meta[name="robots"]').getAttribute('content'), /noindex/);
    if (!session.checkout_available) {
      await payment.getByText('Online checkout is currently unavailable. Please contact Volcan Vacations for help.', {exact:true}).waitFor();
      assert.equal(await payment.locator('#vv-paypal-sdk').count(), 0);
      const attempt = await context.request.post(direct + '/public/payments/paypal/order', {headers:{Authorization:'Bearer '+token}, data:{idempotency_key:randomUUID()}});
      assert.equal(attempt.status(),503);
      console.log('PASS: Missing sandbox credentials block checkout without creating a payment or loading PayPal SDK.');
    } else {
      console.log('Sandbox is configured. This local preflight does not approve or capture PayPal orders; follow the sandbox acceptance guide.');
    }
    const refreshed = admin.waitForResponse(r => r.url().endsWith(`/ops/bookings/${booking.id}/payment`) && r.request().method() === 'GET');
    await admin.getByRole('button', {name:'Refresh payment',exact:true}).click();
    await (await refreshed).finished();
    await admin.getByRole('heading', {name:'Payment record',exact:true}).waitFor();
    await shot(admin,'operations-payment-desktop');
    await admin.getByRole('region', {name:'Payment',exact:true}).screenshot({path:`${output}/operations-payment-panel-desktop.png`});
    await admin.setViewportSize({width:390,height:1000});
    await shot(admin,'operations-payment-mobile');
    await admin.getByRole('region', {name:'Payment',exact:true}).screenshot({path:`${output}/operations-payment-panel-mobile.png`});
    await admin.getByRole('button', {name:'Revoke payment link',exact:true}).click();
    await admin.getByRole('button', {name:'Revoke payment link',exact:true}).waitFor({state:'hidden'});
    assert.equal((await context.request.get(direct+'/public/payments/session',{headers:{Authorization:'Bearer '+token}})).status(),404);
    await payment.reload();
    await payment.locator('.vv-payment').getByRole('alert').waitFor();
    await shot(payment,'revoked-link-mobile');
    await admin.locator('[name="status"]').selectOption('cancelled');
    await admin.getByRole('button', {name:'Save follow-up',exact:true}).click();
    await admin.getByRole('heading', {name:'Not Ready',exact:true}).waitFor();
    await admin.goto(ops+'/payments');
    await admin.getByRole('heading',{name:'Payments',exact:true}).waitFor();
    await shot(admin,'operations-payments-list');
    for (const path of ['/','/tours','/about','/contact','/plan-your-trip','/request?tour='+tour.slug,'/pay']) {
      assert.equal((await publicPage.goto(web+path)).status(),200);
    }
    assert.deepEqual(errors,[]);
    const result={localApplication:'PASS',reference:receipt.reference,bookingId:booking.id,secureTokenAndSnapshot:'PASS',revocation:'PASS',providerMocked:false,
      realSandbox:'NOT TESTED',sandboxBlock:session.checkout_available?'Sandbox approval still requires a buyer acceptance run':'Missing sandbox credentials and webhook ID'};
    fs.writeFileSync(output+'/local-e2e-results.json',JSON.stringify(result,null,2));
    console.log(JSON.stringify(result,null,2));
  } finally {
    if (booking) {
      const current=await request(`/ops/bookings/${booking.id}`);
      await request(`/ops/bookings/${booking.id}`,'PUT',{status:'cancelled',expected_status:current.status,expected_version:current.version,trip_status:'cancelled',internal_notes:'DEMO M5 local acceptance complete; no provider payment made.'});
    }
    if(tour) await request(`/ops/tours/${tour.id}`,'PUT',{...tourBody,active:false,featured:false});
    if(supplier) await request(`/ops/suppliers/${supplier.id}`,'PUT',{...supplierBody,active:false});
    await browser.close();
    console.log('Only test-owned bookings cancelled and test-owned inventory deactivated. No payments simulated or captured.');
  }
})().catch(error=>{console.error(error);process.exit(1);});
