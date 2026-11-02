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
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Starting products import routine...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  log('Target tab: ' + tab.url());
  await tab.bringToFront();

  // Find and click the center Import button
  log('Clicking the Import button in center...');
  const clicked = await tab.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a'));
    const btn = btns.find(b => b.innerText && /import/i.test(b.innerText.trim()));
    if (btn) {
      btn.click();
      return btn.innerText.trim();
    }
    return null;
  });

  log('Clicked Import: ' + clicked);
  await sleep(2500);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/prod_modal_opened.png' });
  log('Saved prod_modal_opened.png');

  // Look for file input
  const fileInput = await tab.$('input[type="file"]');
  if (fileInput) {
    log('Found file input! Attaching rozmiso_products.csv...');
    const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
    await fileInput.uploadFile(csvPath);
    log('Products CSV attached successfully!');
    await sleep(2000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/prod_csv_attached.png' });
    log('Saved prod_csv_attached.png');

    // Click "Upload and continue"
    log('Clicking "Upload and continue"...');
    const clickedContinue = await tab.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.innerText && /upload and continue/i.test(b.innerText.trim()) && !b.disabled);
      if (btn) {
        btn.click();
        return btn.innerText.trim();
      }
      return null;
    });

    log('Clicked continue: ' + clickedContinue);
    await sleep(4000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/prod_preview_screen.png' });
    log('Saved prod_preview_screen.png');

    // Click "Import products" confirmation button
    log('Clicking final "Import products" confirmation...');
    const clickedFinal = await tab.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find(b => b.innerText && /import products/i.test(b.innerText.trim()) && !b.disabled);
      if (btn) {
        btn.click();
        return btn.innerText.trim();
      }
      return null;
    });

    log('Clicked final import button: ' + clickedFinal);
    log('Waiting 10 seconds for product import processing...');
    await sleep(10000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/prod_final_imported.png' });
    log('Saved prod_final_imported.png');
  } else {
    log('File input not found in products modal');
  }

  browser.disconnect();
  log('PRODUCTS_IMPORT_COMPLETE');
}

main().catch(e => log('Fatal: ' + e.message));
