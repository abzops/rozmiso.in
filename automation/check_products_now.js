const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  console.log('Current URL:', tab.url());
  await tab.screenshot({ path: 'f:/Dropshipping/automation/products_now.png' });
  console.log('Saved products_now.png');

  const btns = await tab.evaluate(() => {
    return Array.from(document.querySelectorAll('button, a')).map(b => b.innerText ? b.innerText.trim() : '').filter(t => t.length > 0);
  });
  console.log('All buttons on page:', btns);

  browser.disconnect();
}

main().catch(e => console.error(e));
