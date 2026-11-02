const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runAutoSetup() {
  console.log('====================================================');
  console.log('  Rozmiso Shopify Full Auto-Deployment Bot');
  console.log('====================================================');

  const themeZipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
  const productsCsvPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv');

  console.log('Theme Zip:', themeZipPath, '(Exists:', fs.existsSync(themeZipPath), ')');
  console.log('Products CSV:', productsCsvPath, '(Exists:', fs.existsSync(productsCsvPath), ')');

  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: false,
    userDataDir: 'f:\\Dropshipping\\.chrome-session',
    defaultViewport: null,
    args: [
      '--start-maximized',
      '--no-first-run',
      '--no-default-browser-check'
    ]
  });

  const pages = await browser.pages();
  const page = pages[0] || await browser.newPage();

  const targetDashboard = 'https://dev.shopify.com/dashboard/234984661';
  console.log('\nNavigating to Shopify Partner Dashboard:', targetDashboard);
  await page.goto(targetDashboard, { waitUntil: 'domcontentloaded' });

  console.log('\n[WAITING FOR AUTHENTICATION]');
  console.log('Please log into your Shopify account in the open browser window.');
  console.log('Monitoring URL changes...');

  let authenticated = false;
  while (!authenticated) {
    const url = page.url();
    // When logged in, URL will be at dev.shopify.com/dashboard/... or partners.shopify.com or admin.shopify.com
    if ((url.includes('dev.shopify.com/dashboard') || url.includes('partners.shopify.com/')) &&
        !url.includes('accounts.shopify.com/lookup') &&
        !url.includes('accounts.shopify.com/login')) {
      console.log('>>> Authentication detected! Current URL:', url);
      authenticated = true;
      break;
    }
    await sleep(2000);
  }

  console.log('\n[STEP 1: Dashboard Loaded]');
  await sleep(4000);
  await page.screenshot({ path: 'f:/Dropshipping/automation/step1_dashboard.png' });
  console.log('Saved screenshot: step1_dashboard.png');

  // Navigate to Stores page if not already there
  console.log('\n[STEP 2: Navigating to Stores List]');
  const currentUrl = page.url();
  let partnerIdMatch = currentUrl.match(/dashboard\/(\d+)/) || currentUrl.match(/(\d+)\/stores/);
  let partnerId = partnerIdMatch ? partnerIdMatch[1] : '234984661';

  const storesUrl = `https://dev.shopify.com/dashboard/${partnerId}/stores`;
  console.log('Opening stores URL:', storesUrl);
  await page.goto(storesUrl, { waitUntil: 'networkidle2' }).catch(() => {});
  await sleep(3000);
  await page.screenshot({ path: 'f:/Dropshipping/automation/step2_stores_page.png' });

  console.log('\n[READY FOR ACTIONS]');
  console.log('Browser is active and positioned in your Shopify Partner Dashboard.');
}

runAutoSetup().catch(err => {
  console.error('Auto-setup error:', err);
});
