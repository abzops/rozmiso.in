const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));

  console.log('Target page:', page.url());

  // Find the exact element containing "Import"
  const importCoords = await page.evaluate(() => {
    // Traverse all elements
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let node;
    while (node = walker.nextNode()) {
      if (node.nodeValue && node.nodeValue.trim() === 'Import') {
        const parent = node.parentElement;
        const rect = parent.getBoundingClientRect();
        return {
          tag: parent.tagName,
          rect: { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2, width: rect.width, height: rect.height }
        };
      }
    }
    return null;
  });

  console.log('Import element found:', importCoords);

  if (importCoords) {
    console.log(`Clicking Import at x=${importCoords.rect.x}, y=${importCoords.rect.y}...`);
    await page.mouse.click(importCoords.rect.x, importCoords.rect.y);
    await sleep(1500);

    await page.screenshot({ path: 'f:/Dropshipping/automation/import_dropdown.png' });
    console.log('Saved import_dropdown.png');

    // Check menu items
    const menuItems = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], button, a, span, p'));
      return items.filter(i => /upload|zip|file/i.test(i.innerText || '')).map(i => {
        const r = i.getBoundingClientRect();
        return { text: i.innerText.trim(), x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height };
      });
    });

    console.log('Menu items matching upload/zip:', menuItems);

    if (menuItems.length > 0) {
      const target = menuItems[0];
      console.log(`Clicking "${target.text}" at x=${target.x}, y=${target.y}...`);
      await page.mouse.click(target.x, target.y);
      await sleep(2000);

      await page.screenshot({ path: 'f:/Dropshipping/automation/upload_modal_opened.png' });
      console.log('Saved upload_modal_opened.png');

      // Now attach the zip file to the input[type="file"]
      const fileInput = await page.$('input[type="file"]');
      if (fileInput) {
        console.log('Found file input in modal! Uploading rozmiso-theme.zip...');
        const zipFile = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
        await fileInput.uploadFile(zipFile);
        console.log('File attached!');
        await sleep(2000);

        await page.screenshot({ path: 'f:/Dropshipping/automation/upload_modal_attached.png' });
        console.log('Saved upload_modal_attached.png');

        // Look for the "Upload" or "Upload file" confirmation button
        const uploadConfirmBtn = await page.evaluate(() => {
          const btns = Array.from(document.querySelectorAll('button'));
          const btn = btns.find(b => /upload/i.test(b.innerText || '') && !b.disabled && b.innerText.trim() !== 'Upload zip file');
          if (btn) {
            const r = btn.getBoundingClientRect();
            return { text: btn.innerText.trim(), x: r.x + r.width / 2, y: r.y + r.height / 2 };
          }
          return null;
        });

        console.log('Upload confirmation button:', uploadConfirmBtn);
        if (uploadConfirmBtn) {
          await page.mouse.click(uploadConfirmBtn.x, uploadConfirmBtn.y);
          console.log('Clicked confirmation upload button!');
          await sleep(5000);
          await page.screenshot({ path: 'f:/Dropshipping/automation/theme_uploaded_success.png' });
          console.log('Saved theme_uploaded_success.png');
        }
      }
    }
  } else {
    console.log('Could not find text node "Import".');
  }

  browser.disconnect();
}

main().catch(e => console.error('Error:', e));
