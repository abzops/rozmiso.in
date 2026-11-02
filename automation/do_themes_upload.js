const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function uploadTheme() {
  console.log('Connecting to Chrome...');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const wsEndpoint = 'ws://127.0.0.1:' + content[0] + content[1];

  const browser = await puppeteer.connect({ browserWSEndpoint: wsEndpoint, defaultViewport: null });
  const pages = await browser.pages();
  
  let themePage = pages.find(p => p.url().includes('themes') && !p.url().includes('themes/'));
  if (!themePage) {
    themePage = pages.find(p => p.url().includes('0ghddv-sg'));
  }
  
  if (!themePage) {
    console.log('Theme page not found, creating new page...');
    themePage = await browser.newPage();
    await themePage.goto('https://admin.shopify.com/store/0ghddv-sg/themes', { waitUntil: 'networkidle2' });
  }

  console.log('Active tab:', await themePage.title(), themePage.url());

  // Bring page to front
  await themePage.bringToFront();
  await sleep(2000);

  // Take screenshot of current page
  await themePage.screenshot({ path: 'f:/Dropshipping/automation/themes_current.png' });
  console.log('Saved screenshot to themes_current.png');

  // Let's inspect buttons on the themes page
  const buttons = await themePage.evaluate(() => {
    return Array.from(document.querySelectorAll('button, a')).map(b => ({
      text: b.innerText ? b.innerText.trim() : '',
      ariaLabel: b.getAttribute('aria-label'),
      id: b.id,
      className: b.className
    })).filter(b => b.text || b.ariaLabel);
  });

  console.log('Found buttons:', buttons.filter(b => /theme|add|upload|import|publish/i.test(b.text || b.ariaLabel)));

  browser.disconnect();
}

uploadTheme().catch(e => console.error('Error:', e));
