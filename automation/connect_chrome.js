const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const port = content[0];
  const wsPath = content[1];
  const wsEndpoint = `ws://127.0.0.1:${port}${wsPath}`;

  console.log('Connecting to:', wsEndpoint);

  try {
    const browser = await puppeteer.connect({
      browserWSEndpoint: wsEndpoint,
      defaultViewport: null
    });

    console.log('Successfully connected to Chrome!');
    const pages = await browser.pages();
    console.log(`Total open pages: ${pages.length}`);

    for (let i = 0; i < pages.length; i++) {
      const title = await pages[i].title();
      const url = pages[i].url();
      console.log(`[${i}] Title: "${title}" | URL: "${url}"`);
    }

    // Find the Shopify store page
    let shopifyPage = pages.find(p => p.url().includes('0ghddv-sg') || p.url().includes('admin.shopify.com'));
    if (shopifyPage) {
      console.log('Found Shopify Admin page! Title:', await shopifyPage.title());
      await shopifyPage.screenshot({ path: 'f:/Dropshipping/automation/shopify_admin_tab.png' });
      console.log('Saved screenshot to shopify_admin_tab.png');
    } else {
      console.log('Shopify Admin page not found among open tabs. Looking for any Shopify tab...');
      const anyShopify = pages.find(p => p.url().includes('shopify'));
      if (anyShopify) {
        console.log('Found other Shopify tab:', anyShopify.url());
      }
    }

    browser.disconnect();
  } catch (err) {
    console.error('Error connecting to browser:', err.message);
  }
}

main();
