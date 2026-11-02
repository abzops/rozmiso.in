const puppeteer = require('puppeteer-core');
const fs = require('fs');

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!page) {
    console.error('Shopify tab not found');
    browser.disconnect();
    return;
  }
  await page.bringToFront();

  console.log('Navigating to Themes page...');
  await page.goto('https://admin.shopify.com/store/0ghddv-sg/themes', { waitUntil: 'networkidle2' });
  await sleep(5000);

  await page.screenshot({ path: 'f:/Dropshipping/automation/themes_page_loaded.png' });
  console.log('Saved themes_page_loaded.png');

  // Find frames
  const frames = page.frames();
  console.log(`Found ${frames.length} frames on page:`);
  let themeFrame = null;
  for (const f of frames) {
    console.log(' - Frame URL:', f.url());
    if (f.url().includes('online-store-web.shopifyapps.com/themes')) {
      themeFrame = f;
    }
  }

  const targetContext = themeFrame || page;
  console.log('Inspecting target context:', targetContext.url());

  const themeInfo = await targetContext.evaluate(() => {
    const textNodes = Array.from(document.querySelectorAll('h1, h2, h3, h4, p, span, div')).map(e => e.textContent.trim().replace(/\s+/g, ' ')).filter(t => t.toLowerCase().includes('rozmiso') || t.toLowerCase().includes('theme') || t.toLowerCase().includes('publish'));
    const buttons = Array.from(document.querySelectorAll('button, s-internal-button, a')).map(b => b.textContent.trim().replace(/\s+/g, ' '));
    return {
      matchingTexts: [...new Set(textNodes)].slice(0, 20),
      buttons: [...new Set(buttons)].filter(b => b.length > 0 && b.length < 50)
    };
  });
  console.log('Theme info:', JSON.stringify(themeInfo, null, 2));

  // Look for Publish button
  console.log('Looking for Publish button for rozmiso theme...');
  const publishResult = await targetContext.evaluate(() => {
    // Find containers or cards mentioning rozmiso-theme
    const allElements = Array.from(document.querySelectorAll('*'));
    const rozmisoEl = allElements.find(el => el.textContent && el.textContent.includes('rozmiso-theme') && el.children.length > 0);
    
    // Find all publish buttons
    const btns = Array.from(document.querySelectorAll('button, s-internal-button, a'));
    const publishBtns = btns.filter(b => b.textContent && b.textContent.trim().toLowerCase() === 'publish');
    
    return {
      foundRozmisoContainer: !!rozmisoEl,
      publishButtonsCount: publishBtns.length,
      publishButtons: publishBtns.map(b => ({
        tag: b.tagName,
        text: b.textContent.trim(),
        parentText: b.parentElement ? b.parentElement.textContent.trim().substring(0, 100) : ''
      }))
    };
  });
  console.log('Publish search result:', JSON.stringify(publishResult, null, 2));

  browser.disconnect();
}

run().catch(console.error);
