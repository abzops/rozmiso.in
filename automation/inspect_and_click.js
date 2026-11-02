const puppeteer = require('puppeteer-core');
const fs = require('fs');

function log(msg) {
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Inspecting page elements...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const page = (await browser.pages()).find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));

  // Find all elements on page whose text matches Visit Theme Store or Import
  const found = await page.evaluate(() => {
    const res = [];
    const all = document.querySelectorAll('*');
    for (const el of all) {
      const text = el.innerText || '';
      if (/visit theme store/i.test(text) && el.children.length === 0) {
        const r = el.getBoundingClientRect();
        res.push({ type: 'Visit Theme Store', tag: el.tagName, x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height });
      }
      if (/^import/i.test(text.trim()) && el.children.length === 0) {
        const r = el.getBoundingClientRect();
        res.push({ type: 'Import', tag: el.tagName, x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height });
      }
    }
    return res;
  });

  log('Found targets: ' + JSON.stringify(found, null, 2));

  // If we found "Import", click it!
  const importTarget = found.find(t => t.type === 'Import');
  if (importTarget) {
    log(`Clicking Import at (${importTarget.x}, ${importTarget.y})...`);
    await page.mouse.click(importTarget.x, importTarget.y);
    await sleep(1500);

    await page.screenshot({ path: 'f:/Dropshipping/automation/click1_dropdown.png' });
    log('Captured click1_dropdown.png');

    // Find any menu item
    const menuItems = await page.evaluate(() => {
      const all = Array.from(document.querySelectorAll('*'));
      return all.filter(el => /upload zip file/i.test(el.innerText || '') && el.children.length === 0)
        .map(el => {
          const r = el.getBoundingClientRect();
          return { text: el.innerText.trim(), x: r.x + r.width/2, y: r.y + r.height/2 };
        });
    });

    log('Upload zip options found: ' + JSON.stringify(menuItems, null, 2));
    if (menuItems.length > 0) {
      const item = menuItems[0];
      log(`Clicking "Upload zip file" at (${item.x}, ${item.y})...`);
      await page.mouse.click(item.x, item.y);
      await sleep(2000);

      await page.screenshot({ path: 'f:/Dropshipping/automation/click2_modal.png' });
      log('Captured click2_modal.png');

      // Now attach file
      const fileInput = await page.$('input[type="file"]');
      if (fileInput) {
        log('Attaching file rozmiso-theme.zip...');
        await fileInput.uploadFile('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
        log('Attached file successfully!');
        await sleep(2000);

        await page.screenshot({ path: 'f:/Dropshipping/automation/click3_attached.png' });
        log('Captured click3_attached.png');

        // Click the Upload file button
        const confirmBtn = await page.evaluate(() => {
          const btns = Array.from(document.querySelectorAll('button'));
          const b = btns.find(btn => /^upload file/i.test(btn.innerText || '') && !btn.disabled);
          if (b) {
            const r = b.getBoundingClientRect();
            return { text: b.innerText.trim(), x: r.x + r.width/2, y: r.y + r.height/2 };
          }
          return null;
        });

        log('Confirm button: ' + JSON.stringify(confirmBtn));
        if (confirmBtn) {
          log(`Clicking confirm button at (${confirmBtn.x}, ${confirmBtn.y})...`);
          await page.mouse.click(confirmBtn.x, confirmBtn.y);
          await sleep(6000);
          await page.screenshot({ path: 'f:/Dropshipping/automation/click4_uploaded.png' });
          log('Captured click4_uploaded.png');
        }
      } else {
        log('File input not found in modal');
      }
    }
  } else {
    log('Import target not found.');
  }

  browser.disconnect();
  log('Completed inspect_and_click.');
}

main().catch(e => log('Fatal error: ' + e.message));
