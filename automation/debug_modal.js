const puppeteer = require('puppeteer-core');
const fs = require('fs');

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function debugUploadModal() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  
  const pages = await browser.pages();
  const tab = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!tab) {
    console.log('Tab not found');
    browser.disconnect();
    return;
  }
  await tab.bringToFront();

  console.log('Current URL:', tab.url());
  const frames = tab.frames();
  console.log(`Total frames: ${frames.length}`);
  frames.forEach((f, idx) => console.log(idx, f.url()));

  await tab.screenshot({ path: 'f:/Dropshipping/automation/debug_modal.png' });
  console.log('Saved debug_modal.png');

  for (let i = 0; i < frames.length; i++) {
    const f = frames[i];
    const inputs = await f.evaluate(() => {
      return Array.from(document.querySelectorAll('input, button')).map(el => ({
        tag: el.tagName,
        type: el.type,
        text: el.textContent.trim().substring(0, 50)
      }));
    });
    console.log(`Frame ${i} (${f.url().substring(0, 50)}):`, inputs.filter(x => x.type === 'file' || x.tag === 'BUTTON'));
  }

  browser.disconnect();
}

debugUploadModal().catch(console.error);
