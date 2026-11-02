const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

function log(msg) {
  console.log(msg);
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Started theme upload bot...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const wsEndpoint = 'ws://127.0.0.1:' + content[0] + content[1];

  log('Connecting to: ' + wsEndpoint);
  const browser = await puppeteer.connect({ browserWSEndpoint: wsEndpoint, defaultViewport: null });
  const pages = await browser.pages();
  log('Found ' + pages.length + ' pages');

  const page = pages.find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));
  if (!page) {
    log('ERROR: Themes page not found!');
    browser.disconnect();
    return;
  }

  log('Connected to Themes tab: ' + page.url());

  // Click the Import dropdown button
  log('Searching for Import button...');
  const clicked = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const btn = btns.find(b => b.textContent && b.textContent.trim().toLowerCase().startsWith('import'));
    if (btn) {
      btn.click();
      return btn.textContent.trim();
    }
    return null;
  });

  log('Clicked Import button: ' + clicked);
  await sleep(1500);

  // Look for "Upload zip file" in the opened popover
  log('Searching for "Upload zip file" in popover...');
  const clickedZip = await page.evaluate(() => {
    const elements = Array.from(document.querySelectorAll('button, a, [role="menuitem"], span'));
    const zipEl = elements.find(el => el.textContent && /upload zip file/i.test(el.textContent.trim()));
    if (zipEl) {
      zipEl.click();
      return zipEl.textContent.trim();
    }
    return null;
  });

  log('Clicked "Upload zip file": ' + clickedZip);
  await sleep(2000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/modal_state.png' });
  log('Captured modal_state.png');

  // Look for file input
  const fileInput = await page.$('input[type="file"]');
  if (fileInput) {
    log('Found file input! Attaching f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip...');
    const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
    await fileInput.uploadFile(zipPath);
    log('Theme zip attached successfully!');
    await sleep(2000);

    // Look for submit button
    const submitted = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const uploadBtn = btns.find(b => b.textContent && /^upload/i.test(b.textContent.trim()) && !b.disabled);
      if (uploadBtn) {
        uploadBtn.click();
        return uploadBtn.textContent.trim();
      }
      return null;
    });

    log('Clicked submit button: ' + submitted);
    await sleep(6000);
    await page.screenshot({ path: 'f:/Dropshipping/automation/after_theme_submit.png' });
    log('Captured after_theme_submit.png');
  } else {
    log('File input not found yet in modal');
  }

  browser.disconnect();
  log('Done!');
}

main().catch(e => log('Error: ' + e.message));
