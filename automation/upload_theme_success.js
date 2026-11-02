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
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Starting precise theme upload...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const tab = pages[0]; // Tab 0 is the themes page

  log('Tab 0: ' + tab.url());
  await tab.bringToFront();
  await sleep(1000);

  // Find the themes frame
  const frame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?'));
  if (!frame) {
    log('ERROR: Themes frame not found among ' + tab.frames().length + ' frames');
    browser.disconnect();
    return;
  }

  log('Target frame found: ' + frame.url().substring(0, 80) + '...');

  // Click "Upload zip file"
  log('Clicking "Upload zip file" inside frame...');
  const clicked = await frame.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a, span, p'));
    const zipBtn = btns.find(b => b.innerText && /upload zip file/i.test(b.innerText.trim()));
    if (zipBtn) {
      zipBtn.click();
      return zipBtn.innerText.trim();
    }
    return null;
  });

  log('Clicked result: ' + clicked);
  await sleep(2500);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_step1_clicked.png' });
  log('Captured theme_step1_clicked.png');

  // Look for input[type="file"] in all frames and root
  let fileInput = null;
  for (const f of tab.frames()) {
    fileInput = await f.$('input[type="file"]');
    if (fileInput) {
      log('Found file input in frame: ' + f.url().substring(0, 60));
      break;
    }
  }
  if (!fileInput) {
    fileInput = await tab.$('input[type="file"]');
    if (fileInput) log('Found file input in main tab');
  }

  if (fileInput) {
    log('Attaching rozmiso-theme.zip...');
    const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
    await fileInput.uploadFile(zipPath);
    log('File attached successfully!');
    await sleep(2000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_step2_attached.png' });
    log('Captured theme_step2_attached.png');

    // Find and click the confirm button (e.g. "Upload file")
    log('Looking for confirm upload button...');
    let submitted = false;
    for (const f of tab.frames()) {
      const res = await f.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(btn => btn.innerText && /^upload file/i.test(btn.innerText.trim()) && !btn.disabled);
        if (b) {
          b.click();
          return b.innerText.trim();
        }
        return null;
      });
      if (res) {
        log('Clicked confirm in frame: ' + res);
        submitted = true;
        break;
      }
    }

    if (!submitted) {
      const res = await tab.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(btn => btn.innerText && /^upload file/i.test(btn.innerText.trim()) && !btn.disabled);
        if (b) {
          b.click();
          return b.innerText.trim();
        }
        return null;
      });
      if (res) log('Clicked confirm in main tab: ' + res);
    }

    log('Waiting 12 seconds for theme to upload and unpack...');
    await sleep(12000);

    await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_step3_uploaded.png' });
    log('Captured theme_step3_uploaded.png');
  } else {
    log('ERROR: File input was not found in any frame!');
  }

  browser.disconnect();
  log('FINISHED_THEME_UPLOAD');
}

main().catch(e => log('Fatal: ' + e.message));
