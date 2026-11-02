const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function log(msg) {
  console.log(msg);
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function main() {
  log('--- Starting upload and publish flow ---');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const tab = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!tab) {
    log('ERROR: Shopify tab not found');
    browser.disconnect();
    return;
  }
  await tab.bringToFront();

  // 1. Navigate to themes
  log('Navigating to themes page...');
  await tab.goto('https://admin.shopify.com/store/0ghddv-sg/themes', { waitUntil: 'networkidle2' });
  await sleep(4000);

  // 2. Find themes frame
  const frame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?'));
  if (!frame) {
    log('ERROR: Themes frame not found');
    browser.disconnect();
    return;
  }

  // 3. Click "Upload zip file"
  log('Clicking "Upload zip file" button...');
  const clickedUploadZip = await frame.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a, span, p'));
    const b = btns.find(el => el.innerText && /upload zip file/i.test(el.innerText.trim()));
    if (b) {
      b.click();
      return b.innerText.trim();
    }
    return null;
  });
  log('Upload zip clicked: ' + clickedUploadZip);
  await sleep(2500);

  // 4. Find file input across frames
  let fileInput = null;
  for (const f of tab.frames()) {
    fileInput = await f.$('input[type="file"]');
    if (fileInput) break;
  }
  if (!fileInput) fileInput = await tab.$('input[type="file"]');

  if (!fileInput) {
    log('ERROR: File input not found for zip');
    browser.disconnect();
    return;
  }

  const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
  log('Uploading zip: ' + zipPath);
  await fileInput.uploadFile(zipPath);
  await sleep(2500);

  // 5. Click "Upload file" confirmation button
  log('Confirming upload...');
  let clickedConfirm = false;
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
      log('Clicked upload confirm in frame: ' + res);
      clickedConfirm = true;
      break;
    }
  }

  log('Waiting 15 seconds for Shopify to process the new theme zip...');
  await sleep(15000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_uploaded_new.png' });
  log('Saved theme_uploaded_new.png');

  // 6. Look for the newly added draft theme's Publish button
  log('Finding newly uploaded theme in draft list to publish...');
  const targetFrame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?')) || frame;
  
  const publishClicked = await targetFrame.evaluate(() => {
    // In the draft themes section, look for Publish buttons
    const btns = Array.from(document.querySelectorAll('button, s-internal-button'));
    const pubBtns = btns.filter(b => b.textContent && b.textContent.trim().toLowerCase() === 'publish');
    if (pubBtns.length > 0) {
      // The newest uploaded theme is typically the first draft theme
      const firstPub = pubBtns[0];
      firstPub.click();
      if (firstPub.shadowRoot) {
        const inner = firstPub.shadowRoot.querySelector('button');
        if (inner) inner.click();
      }
      return 'Clicked Publish button (total found: ' + pubBtns.length + ')';
    }
    return null;
  });
  log('Publish button click: ' + publishClicked);
  await sleep(3000);

  // 7. Check if a publish confirmation modal appeared
  log('Checking for publish confirmation modal...');
  let modalPublishClicked = false;
  for (const f of tab.frames()) {
    const res = await f.evaluate(() => {
      const dialog = document.querySelector('[role="dialog"], s-modal, s-dialog');
      if (dialog) {
        const btns = Array.from(dialog.querySelectorAll('button, s-internal-button'));
        const pub = btns.find(b => b.textContent && b.textContent.trim().toLowerCase() === 'publish');
        if (pub) {
          pub.click();
          if (pub.shadowRoot) {
            const inner = pub.shadowRoot.querySelector('button');
            if (inner) inner.click();
          }
          return 'Confirmed publish in dialog';
        }
      }
      return null;
    });
    if (res) {
      log('Modal confirmation: ' + res);
      modalPublishClicked = true;
      break;
    }
  }

  if (!modalPublishClicked) {
    const res = await tab.evaluate(() => {
      const dialog = document.querySelector('[role="dialog"], s-modal, s-dialog');
      if (dialog) {
        const btns = Array.from(dialog.querySelectorAll('button, s-internal-button'));
        const pub = btns.find(b => b.textContent && b.textContent.trim().toLowerCase() === 'publish');
        if (pub) {
          pub.click();
          if (pub.shadowRoot) {
            const inner = pub.shadowRoot.querySelector('button');
            if (inner) inner.click();
          }
          return 'Confirmed publish in main dialog';
        }
      }
      return null;
    });
    if (res) log('Modal confirmation main: ' + res);
  }

  log('Waiting 8 seconds for theme activation...');
  await sleep(8000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/theme_published_live.png' });
  log('Saved theme_published_live.png');

  browser.disconnect();
  log('UPLOAD_AND_PUBLISH_FINISHED');
}

main().catch(e => log('Fatal error in theme upload/publish: ' + e.message));
