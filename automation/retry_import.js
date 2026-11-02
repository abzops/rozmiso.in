const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!page) {
    console.error('Shopify tab not found');
    browser.disconnect();
    return;
  }
  await page.bringToFront();

  console.log('Navigating cleanly to Products...');
  await page.goto('https://admin.shopify.com/store/0ghddv-sg/products', { waitUntil: 'networkidle2' });
  await sleep(3000);

  // Click Import
  console.log('Clicking Import button...');
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button, a'));
    for (const b of btns) {
      if (b.textContent && b.textContent.trim().toLowerCase() === 'import') {
        b.click();
        if (b.shadowRoot) {
          const inner = b.shadowRoot.querySelector('button');
          if (inner) inner.click();
        }
        return true;
      }
    }
    return false;
  });
  await sleep(2500);

  // Find file input
  console.log('Attaching newly generated rozmiso_products.csv...');
  const fileInput = await page.$('input[type="file"]');
  if (!fileInput) {
    console.error('File input not found!');
    await page.screenshot({ path: 'f:/Dropshipping/automation/retry_no_file_input.png' });
    browser.disconnect();
    return;
  }

  const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
  await fileInput.uploadFile(csvPath);
  console.log('File uploaded:', csvPath);
  await sleep(2500);

  await page.screenshot({ path: 'f:/Dropshipping/automation/retry_file_attached.png' });

  // Click Upload file
  console.log('Clicking Upload file button...');
  const uploadClicked = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button'));
    for (const b of btns) {
      if (b.textContent && b.textContent.trim().toLowerCase() === 'upload file') {
        b.click();
        if (b.shadowRoot) {
          const inner = b.shadowRoot.querySelector('button');
          if (inner) inner.click();
        }
        return true;
      }
    }
    return false;
  });
  console.log('Upload button clicked:', uploadClicked);

  console.log('Waiting 6 seconds for preview screen...');
  await sleep(6000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/retry_preview_screen.png' });

  const previewInfo = await page.evaluate(() => {
    const dialogs = Array.from(document.querySelectorAll('[role="dialog"], s-modal, s-dialog')).map(d => d.textContent.trim().replace(/\s+/g, ' '));
    const btns = Array.from(document.querySelectorAll('button, s-internal-button')).map(b => b.textContent.trim().replace(/\s+/g, ' '));
    return { dialogs, btns: [...new Set(btns)].filter(b => b.length > 0 && b.length < 50) };
  });
  console.log('Preview Screen info:', JSON.stringify(previewInfo, null, 2));

  // Click Import products
  console.log('Clicking "Import products" confirmation button...');
  const confirmed = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button'));
    for (const b of btns) {
      const txt = b.textContent.trim().toLowerCase();
      if (txt === 'import products' || txt.includes('import products')) {
        b.click();
        if (b.shadowRoot) {
          const inner = b.shadowRoot.querySelector('button');
          if (inner) inner.click();
        }
        return b.textContent.trim();
      }
    }
    return null;
  });
  console.log('Confirmed click result:', confirmed);

  console.log('Waiting 15 seconds for Shopify import process...');
  await sleep(15000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/retry_import_final.png' });
  console.log('Saved retry_import_final.png');

  browser.disconnect();
  console.log('RETRY_IMPORT_DONE');
}

run().catch(console.error);
