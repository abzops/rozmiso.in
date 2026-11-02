const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function inspectTab() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();
  const page = pages.find(p => p.url().includes('admin.shopify.com/store/0ghddv-sg'));
  if (!page) {
    console.log('Shopify tab not found');
    browser.disconnect();
    return;
  }
  await page.screenshot({ path: 'f:/Dropshipping/automation/current_products_tab.png' });
  console.log('Saved f:/Dropshipping/automation/current_products_tab.png');
  
  const textInfo = await page.evaluate(() => {
    const buttons = Array.from(document.querySelectorAll('button, s-internal-button')).map(b => b.textContent ? b.textContent.trim().replace(/\s+/g, ' ') : '');
    const textNodes = Array.from(document.querySelectorAll('h1, h2, h3, p, span')).map(e => e.textContent ? e.textContent.trim().replace(/\s+/g, ' ') : '').filter(t => t.length > 5 && t.length < 100);
    return {
      title: document.title,
      buttons: [...new Set(buttons)].filter(Boolean),
      sampleTexts: [...new Set(textNodes)].slice(0, 30)
    };
  });
  console.log('Page info:', JSON.stringify(textInfo, null, 2));
  browser.disconnect();
}
inspectTab().catch(console.error);
