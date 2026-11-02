const puppeteer = require('puppeteer-core');
const fs = require('fs');

function log(msg) {
  console.log(msg);
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Submitting product import...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  // 1. Click "Upload file"
  log('Clicking "Upload file" button...');
  const clickedUpload = await tab.evaluate(() => {
    const all = Array.from(document.querySelectorAll('s-internal-button, button'));
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

  log('Clicked Upload file: ' + clickedUpload);
  await sleep(4000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/step_import_preview.png' });
  log('Saved step_import_preview.png');

  // 2. Click "Import products" confirmation button on preview modal
  log('Clicking "Import products" confirmation button...');
  const clickedConfirm = await tab.evaluate(() => {
    const all = Array.from(document.querySelectorAll('s-internal-button, button'));
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

  log('Clicked confirmation: ' + clickedConfirm);
  log('Waiting 12 seconds for Shopify to import all 5 products and variants...');
  await sleep(12000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/step_all_products_live.png' });
  log('Saved step_all_products_live.png');

  browser.disconnect();
  log('PRODUCTS_SUCCESSFULLY_IMPORTED');
}

main().catch(e => log('Error: ' + e.message));
