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
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Publishing theme and importing products...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  log('Tab: ' + tab.url());
  await tab.bringToFront();

  // 1. Publish the uploaded Rozmiso theme
  log('Publishing rozmiso-theme...');
  const themeFrame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?'));
  if (themeFrame) {
    const publishedClicked = await themeFrame.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const pubBtn = btns.find(b => b.innerText && /^publish/i.test(b.innerText.trim()));
      if (pubBtn) {
        pubBtn.click();
        return pubBtn.innerText.trim();
      }
      return null;
    });
    log('Clicked publish button in iframe: ' + publishedClicked);
    await sleep(2000);

    // Click confirm publish modal if present
    const confirmPub = await tab.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const pubBtn = btns.find(b => b.innerText && /^publish/i.test(b.innerText.trim()) && !b.innerText.includes('Publish v'));
      if (pubBtn) {
        pubBtn.click();
        return pubBtn.innerText.trim();
      }
      return null;
    });
    log('Clicked publish confirmation: ' + confirmPub);
    await sleep(4000);
    await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_published.png' });
    log('Saved theme_published.png');
  }

  // 2. Navigate to Products page
  log('Navigating to Products page: https://admin.shopify.com/store/0ghddv-sg/products');
  await tab.goto('https://admin.shopify.com/store/0ghddv-sg/products', { waitUntil: 'networkidle2' });
  await sleep(3000);
  await tab.screenshot({ path: 'f:/Dropshipping/automation/products_page.png' });
  log('Saved products_page.png');

  // Look for Import button on products page
  log('Looking for Import button on Products page...');
  const importClicked = await tab.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a'));
    const impBtn = btns.find(b => b.innerText && /^import/i.test(b.innerText.trim()));
    if (impBtn) {
      impBtn.click();
      return impBtn.innerText.trim();
    }
    return null;
  });
  log('Clicked Products Import button: ' + importClicked);
  await sleep(2500);
  await tab.screenshot({ path: 'f:/Dropshipping/automation/products_import_modal.png' });
  log('Saved products_import_modal.png');

  // Find file input in products modal
  let fileInput = await tab.$('input[type="file"]');
  if (!fileInput) {
    for (const f of tab.frames()) {
      fileInput = await f.$('input[type="file"]');
      if (fileInput) break;
    }
  }

  if (fileInput) {
    log('Attaching rozmiso_products.csv...');
    const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
    await fileInput.uploadFile(csvPath);
    log('Attached products CSV!');
    await sleep(2000);
    await tab.screenshot({ path: 'f:/Dropshipping/automation/products_csv_attached.png' });
    log('Saved products_csv_attached.png');

    // Click "Upload and continue" button
    const uploadAndContinue = await tab.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.innerText && /upload and continue/i.test(b.innerText.trim()) && !b.disabled);
      if (btn) {
        btn.click();
        return btn.innerText.trim();
      }
      return null;
    });
    log('Clicked Upload and continue: ' + uploadAndContinue);
    await sleep(4000);
    await tab.screenshot({ path: 'f:/Dropshipping/automation/products_preview_step.png' });
    log('Saved products_preview_step.png');

    // Click "Import products" confirmation button
    const importConfirm = await tab.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.innerText && /import products/i.test(b.innerText.trim()) && !b.disabled);
      if (btn) {
        btn.click();
        return btn.innerText.trim();
      }
      return null;
    });
    log('Clicked Import products confirmation: ' + importConfirm);
    await sleep(6000);
    await tab.screenshot({ path: 'f:/Dropshipping/automation/products_imported_success.png' });
    log('Saved products_imported_success.png');
  } else {
    log('File input not found on Products import modal');
  }

  browser.disconnect();
  log('FINISHED_ALL_TASKS');
}

main().catch(e => log('Fatal error: ' + e.message));
