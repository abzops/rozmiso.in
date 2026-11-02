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
  log('=== Starting Standard POSIX Theme Upload & Activation ===');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  
  const pages = await browser.pages();
  let tab = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!tab) {
    tab = await browser.newPage();
  }
  await tab.bringToFront();

  log('Navigating freshly to Themes...');
  await tab.goto('https://admin.shopify.com/store/0ghddv-sg/themes', { waitUntil: 'networkidle2' });
  await sleep(6000);

  // Find themes frame
  let frame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?'));
  if (!frame) {
    await sleep(4000);
    frame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?'));
  }

  if (!frame) {
    log('ERROR: Themes frame not found');
    browser.disconnect();
    return;
  }

  log('Themes frame located: ' + frame.url().substring(0, 60));

  // Click "Upload zip file"
  log('Clicking "Upload zip file" button inside frame...');
  const clickedUpload = await frame.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a, span, p'));
    const zipBtn = btns.find(b => b.innerText && /upload zip file/i.test(b.innerText.trim()));
    if (zipBtn) {
      zipBtn.click();
      return zipBtn.innerText.trim();
    }
    return null;
  });
  log('Upload zip clicked: ' + clickedUpload);
  await sleep(2500);

  // Find file input across frames
  let fileInput = null;
  for (const f of tab.frames()) {
    fileInput = await f.$('input[type="file"]');
    if (fileInput) {
      log('Found file input in frame: ' + f.url().substring(0, 50));
      break;
    }
  }
  if (!fileInput) fileInput = await tab.$('input[type="file"]');

  if (!fileInput) {
    log('ERROR: File input not found!');
    browser.disconnect();
    return;
  }

  const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
  log('Attaching POSIX zip: ' + zipPath);
  await fileInput.uploadFile(zipPath);
  await sleep(2500);

  // Click "Upload file" confirmation button
  log('Clicking confirm "Upload file" button...');
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
      log('Submitted upload in frame: ' + res);
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
    if (res) log('Submitted upload in main: ' + res);
  }

  log('Waiting 18 seconds for Shopify to validate and install theme...');
  await sleep(18000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/step5_upload_result.png' });
  log('Saved step5_upload_result.png');

  // Look for Publish button
  const currentFrame = tab.frames().find(f => f.url().startsWith('https://online-store-web.shopifyapps.com/themes?')) || frame;
  log('Looking for Publish button on the newly added theme...');
  const publishClicked = await currentFrame.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button'));
    const pubBtns = btns.filter(b => b.textContent && b.textContent.trim().toLowerCase() === 'publish');
    if (pubBtns.length > 0) {
      const firstPub = pubBtns[0];
      firstPub.click();
      if (firstPub.shadowRoot) {
        const inner = firstPub.shadowRoot.querySelector('button');
        if (inner) inner.click();
      }
      return 'Clicked Publish (total found: ' + pubBtns.length + ')';
    }
    return null;
  });
  log('Publish button result: ' + publishClicked);
  await sleep(3000);

  // Confirm publish inside modal
  log('Confirming publish inside modal...');
  for (const f of tab.frames()) {
    await f.evaluate(() => {
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
        }
      }
    });
  }

  log('Waiting 10 seconds for activation...');
  await sleep(10000);

  await tab.screenshot({ path: 'f:/Dropshipping/automation/step6_published_final.png' });
  log('Saved step6_published_final.png');

  browser.disconnect();
  log('FLIPKART_THEME_DEPLOYMENT_COMPLETE');
}

main().catch(e => log('Fatal: ' + e.message));
