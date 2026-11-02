const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

function log(msg) {
  console.log(msg);
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Starting one-flow product import...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  log('Target tab: ' + tab.url());
  await tab.bringToFront();

  // 1. Click Import button
  log('Step 1: Clicking Import button...');
  const clickedImport = await tab.evaluate(() => {
    const sBtns = Array.from(document.querySelectorAll('s-internal-button, button'));
    const imp = sBtns.find(b => b.textContent && b.textContent.trim().toLowerCase() === 'import');
    if (imp) {
      imp.click();
      if (imp.shadowRoot) {
        const btn = imp.shadowRoot.querySelector('button');
        if (btn) btn.click();
      }
      return true;
    }
    return false;
  });

  log('Clicked import button: ' + clickedImport);
  await sleep(2500);

  // 2. Attach CSV file
  log('Step 2: Attaching CSV file...');
  const fileInput = await tab.$('input[type="file"]');
  if (!fileInput) {
    log('ERROR: File input not found!');
    browser.disconnect();
    return;
  }

  const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
  await fileInput.uploadFile(csvPath);
  log('CSV attached: ' + csvPath);
  await sleep(2500);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/flow_step1_attached.png' });
  log('Saved flow_step1_attached.png');

  // 3. Click "Upload file" inside modal
  log('Step 3: Finding and clicking "Upload file"...');
  const clickedUpload = await tab.evaluate(() => {
    const all = Array.from(document.querySelectorAll('s-internal-button, button, a'));
    const btn = all.find(b => b.textContent && /^upload file/i.test(b.textContent.trim()));
    if (btn) {
      btn.click();
      if (btn.shadowRoot) {
        const inner = btn.shadowRoot.querySelector('button');
        if (inner) inner.click();
      }
      return btn.textContent.trim();
    }
    return null;
  });

  log('Clicked Upload button result: ' + clickedUpload);
  await sleep(4000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/flow_step2_preview.png' });
  log('Saved flow_step2_preview.png');

  // 4. Click "Import products" confirmation button on preview screen
  log('Step 4: Finding and clicking "Import products"...');
  const clickedConfirm = await tab.evaluate(() => {
    const all = Array.from(document.querySelectorAll('s-internal-button, button, a'));
    const btn = all.find(b => b.textContent && /^import products/i.test(b.textContent.trim()));
    if (btn) {
      btn.click();
      if (btn.shadowRoot) {
        const inner = btn.shadowRoot.querySelector('button');
        if (inner) inner.click();
      }
      return btn.textContent.trim();
    }
    return null;
  });

  log('Clicked Confirm button result: ' + clickedConfirm);
  log('Step 5: Waiting 15 seconds for Shopify to finish importing products...');
  await sleep(15000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/flow_step3_complete.png' });
  log('Saved flow_step3_complete.png');

  browser.disconnect();
  log('PRODUCT_IMPORT_FULLY_COMPLETE');
}

main().catch(e => log('Fatal error: ' + e.message));
