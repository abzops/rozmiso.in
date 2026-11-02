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
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Clicking s-internal-button Import...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  log('Tab: ' + tab.url());
  await tab.bringToFront();

  // Find and click the <s-internal-button> containing "Import"
  const clicked = await tab.evaluate(() => {
    const sBtns = Array.from(document.querySelectorAll('s-internal-button, button'));
    const imp = sBtns.find(b => b.textContent && b.textContent.trim().toLowerCase() === 'import');
    if (imp) {
      imp.click();
      // If it has shadowRoot or inner button, click that too
      if (imp.shadowRoot) {
        const inner = imp.shadowRoot.querySelector('button');
        if (inner) inner.click();
      }
      return 'Found and clicked: ' + imp.tagName;
    }
    return 'Not found';
  });

  log('Click result: ' + clicked);
  await sleep(2500);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/step_import_modal.png' });
  log('Saved step_import_modal.png');

  // Look for file input across document and shadow roots
  let fileInput = await tab.$('input[type="file"]');
  log('Direct file input found: ' + (fileInput ? 'YES' : 'NO'));

  if (!fileInput) {
    // Check inside shadow roots or custom elements
    const fileInputSelector = await tab.evaluate(() => {
      const inputs = Array.from(document.querySelectorAll('input[type="file"]'));
      if (inputs.length > 0) return 'input[type="file"]';
      // Look in shadow roots
      const all = Array.from(document.querySelectorAll('*'));
      for (const el of all) {
        if (el.shadowRoot) {
          const inp = el.shadowRoot.querySelector('input[type="file"]');
          if (inp) return el.tagName;
        }
      }
      return null;
    });
    log('Shadow root search: ' + fileInputSelector);
  }

  if (fileInput) {
    const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
    log('Uploading: ' + csvPath);
    await fileInput.uploadFile(csvPath);
    log('Products CSV attached successfully!');
    await sleep(2500);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/step_csv_attached.png' });
    log('Saved step_csv_attached.png');

    // Click "Upload and continue" button
    const contClicked = await tab.evaluate(() => {
      const allBtns = Array.from(document.querySelectorAll('s-internal-button, button'));
      const btn = allBtns.find(b => b.textContent && /upload and continue/i.test(b.textContent.trim()));
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

    log('Clicked continue: ' + contClicked);
    await sleep(4000);
    await tab.screenshot({ path: 'f:/Dropshipping/automation/step_preview.png' });
    log('Saved step_preview.png');

    // Click final "Import products" confirmation button
    const finalClicked = await tab.evaluate(() => {
      const allBtns = Array.from(document.querySelectorAll('s-internal-button, button'));
      const btn = allBtns.find(b => b.textContent && /import products/i.test(b.textContent.trim()));
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

    log('Clicked final import button: ' + finalClicked);
    log('Waiting 10 seconds for import to finish...');
    await sleep(10000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/step_products_imported.png' });
    log('Saved step_products_imported.png');
  }

  browser.disconnect();
  log('PRODUCTS_IMPORT_ROUTINE_FINISHED');
}

main().catch(e => log('Fatal: ' + e.message));
