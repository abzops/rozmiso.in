const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

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
  console.log('On products page:', page.url());

  // 1. Click Import button
  console.log('Clicking Import button...');
  const clicked = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, s-internal-button, a'));
    for (const b of btns) {
      if (b.textContent && b.textContent.trim().toLowerCase() === 'import') {
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
  console.log('Import clicked:', clicked);
  await sleep(2000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/import_dialog_open.png' });
  console.log('Saved import_dialog_open.png');

  // Check what modal or file inputs exist
  const modalInfo = await page.evaluate(() => {
    const fileInputs = Array.from(document.querySelectorAll('input[type="file"]')).map(i => ({
      id: i.id,
      name: i.name,
      accept: i.accept,
      visible: i.offsetParent !== null
    }));
    const dialogs = Array.from(document.querySelectorAll('[role="dialog"], s-modal, s-dialog, s-sheet')).map(d => ({
      tag: d.tagName,
      role: d.getAttribute('role'),
      text: d.textContent.trim().substring(0, 300)
    }));
    const buttons = Array.from(document.querySelectorAll('button, s-internal-button')).map(b => b.textContent.trim().replace(/\s+/g, ' '));
    return { fileInputs, dialogs, buttons: [...new Set(buttons)] };
  });
  console.log('Modal info:', JSON.stringify(modalInfo, null, 2));

  // Find file input and upload
  const fileInput = await page.$('input[type="file"]');
  if (!fileInput) {
    console.error('No input[type="file"] found on page or shadow DOM');
    // Check shadow roots if needed
  } else {
    const csvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');
    console.log('Attaching file:', csvPath);
    await fileInput.uploadFile(csvPath);
    await sleep(2500);

    await page.screenshot({ path: 'f:/Dropshipping/automation/import_file_attached.png' });
    console.log('Saved import_file_attached.png');

    // Check buttons again
    const postAttachButtons = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, s-internal-button, a')).map(b => ({
        tag: b.tagName,
        text: b.textContent.trim().replace(/\s+/g, ' '),
        disabled: b.disabled || b.hasAttribute('disabled') || b.getAttribute('aria-disabled') === 'true'
      }));
    });
    console.log('Post-attach buttons:', JSON.stringify(postAttachButtons.filter(b => b.text.length > 0 && b.text.length < 50), null, 2));
  }

  browser.disconnect();
}

run().catch(console.error);
