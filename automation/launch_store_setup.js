const puppeteer = require('puppeteer-core');
const path = require('path');

async function testLaunch() {
  console.log('Testing launch of visible Chrome...');
  try {
    const browser = await puppeteer.launch({
      executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      headless: false,
      userDataDir: 'f:\\Dropshipping\\.chrome-session',
      defaultViewport: null,
      args: [
        '--remote-debugging-port=9333',
        '--no-first-run',
        '--no-default-browser-check',
        'https://dev.shopify.com/dashboard/234984661'
      ]
    });
    console.log('Browser launched successfully!');
    const pages = await browser.pages();
    const page = pages[0] || await browser.newPage();
    console.log('Page navigated to:', page.url());
    
    // Keep it open or report back
    console.log('Title:', await page.title());
  } catch (err) {
    console.error('Launch failed:', err.message);
  }
}

testLaunch();
