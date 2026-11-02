const puppeteer = require('puppeteer-core');
const fs = require('fs');

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg/products'));
  if (!page) {
    console.error('Products tab not found');
    browser.disconnect();
    return;
  }
  await page.bringToFront();

  // 1. Click "Upload file"
  console.log('Clicking "Upload file" button...');
  const clickedUpload = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button, input[type="button"], input[type="submit"]'));
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
  console.log('Upload file clicked:', clickedUpload);

  console.log('Waiting 5 seconds for CSV preview to load...');
  await sleep(5000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/import_preview_dialog.png' });
  console.log('Saved import_preview_dialog.png');

  // Inspect the preview dialog
  const previewState = await page.evaluate(() => {
    const dialogs = Array.from(document.querySelectorAll('[role="dialog"], s-modal, s-dialog')).map(d => d.textContent.trim().replace(/\s+/g, ' '));
    const buttons = Array.from(document.querySelectorAll('button, s-internal-button')).map(b => ({
      text: b.textContent.trim().replace(/\s+/g, ' '),
      tag: b.tagName
    }));
    return { dialogs, buttons: buttons.filter(b => b.text.length > 0 && b.text.length < 50) };
  });
  console.log('Preview state:', JSON.stringify(previewState, null, 2));

  // Find and click "Import products" or similar confirm button
  console.log('Looking for confirmation button...');
  const clickedConfirm = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button'));
    for (const b of btns) {
      const txt = b.textContent.trim().toLowerCase();
      if (txt.includes('import product') || txt.includes('import') && !txt.includes('cancel')) {
        // Prefer the primary button
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
  console.log('Clicked confirmation:', clickedConfirm);

  console.log('Waiting 10 seconds for import processing...');
  await sleep(10000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/import_final_state.png' });
  console.log('Saved import_final_state.png');

  browser.disconnect();
}

run().catch(console.error);
