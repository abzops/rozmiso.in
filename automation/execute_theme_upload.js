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
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Starting direct iframe theme upload...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const page = (await browser.pages()).find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));

  const themeFrame = page.frames().find(f => f.url().includes('online-store-web.shopifyapps.com/themes'));
  if (!themeFrame) {
    log('ERROR: Theme iframe not found!');
    browser.disconnect();
    return;
  }

  log('Targeting Theme iframe: ' + themeFrame.url());

  // Click the "Upload zip file" button inside themeFrame
  log('Clicking "Upload zip file" button inside iframe...');
  const clicked = await themeFrame.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a, span'));
    const zipBtn = btns.find(b => b.innerText && /upload zip file/i.test(b.innerText.trim()));
    if (zipBtn) {
      zipBtn.click();
      return zipBtn.innerText.trim();
    }
    return null;
  });

  log('Clicked: ' + clicked);
  await sleep(2000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/step_modal_opened.png' });
  log('Saved step_modal_opened.png');

  // Check for file input across all frames and page
  let fileInput = await themeFrame.$('input[type="file"]');
  if (!fileInput) {
    fileInput = await page.$('input[type="file"]');
  }
  if (!fileInput) {
    for (const f of page.frames()) {
      fileInput = await f.$('input[type="file"]');
      if (fileInput) {
        log('Found file input in frame: ' + f.url());
        break;
      }
    }
  }

  if (fileInput) {
    log('Found file input element! Uploading rozmiso-theme.zip...');
    const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
    await fileInput.uploadFile(zipPath);
    log('File attached!');
    await sleep(2000);

    await page.screenshot({ path: 'f:/Dropshipping/automation/step_file_attached.png' });
    log('Saved step_file_attached.png');

    // Click confirmation submit button (e.g. "Upload file")
    log('Searching for confirmation Upload button...');
    const submitted = await page.evaluate(() => {
      // Check in main document first
      const btns = Array.from(document.querySelectorAll('button'));
      const uploadBtn = btns.find(b => b.innerText && /^upload file/i.test(b.innerText.trim()) && !b.disabled);
      if (uploadBtn) {
        uploadBtn.click();
        return uploadBtn.innerText.trim();
      }
      return null;
    });

    log('Submitted via page: ' + submitted);
    if (!submitted) {
      const subFrame = await themeFrame.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const uploadBtn = btns.find(b => b.innerText && /^upload file/i.test(b.innerText.trim()) && !b.disabled);
        if (uploadBtn) {
          uploadBtn.click();
          return uploadBtn.innerText.trim();
        }
        return null;
      });
      log('Submitted via iframe: ' + subFrame);
    }

    log('Waiting for theme upload processing (10 seconds)...');
    await sleep(10000);
    await page.screenshot({ path: 'f:/Dropshipping/automation/step_theme_uploaded.png' });
    log('Saved step_theme_uploaded.png');
  } else {
    log('File input not found.');
  }

  browser.disconnect();
  log('SUCCESS! Finished theme upload routine.');
}

main().catch(e => log('Error: ' + e.message));
