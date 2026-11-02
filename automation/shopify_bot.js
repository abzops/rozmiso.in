const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runBot() {
  console.log('--- Rozmiso Shopify Automated Assistant ---');
  console.log('Connecting to active automated Chrome session on port 9333...');

  let browser;
  try {
    browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9333',
      defaultViewport: null
    });
  } catch (e) {
    console.error('Could not connect to browser on port 9333:', e.message);
    return;
  }

  console.log('Successfully connected to Chrome!');
  const pages = await browser.pages();
  let page = pages[0];

  console.log('Monitoring page URL:', page.url());
  console.log('Waiting for user to log in...');

  // Loop until authenticated
  let isLoggedIn = false;
  for (let attempt = 0; attempt < 120; attempt++) {
    const currentUrl = page.url();
    if (currentUrl.includes('dev.shopify.com') || currentUrl.includes('admin.shopify.com') || currentUrl.includes('partners.shopify.com')) {
      if (!currentUrl.includes('accounts.shopify.com/lookup') && !currentUrl.includes('accounts.shopify.com/login')) {
        console.log('✅ Login detected! Current URL:', currentUrl);
        isLoggedIn = true;
        break;
      }
    }
    await sleep(2000);
  }

  if (!isLoggedIn) {
    console.log('⏱️ Login timed out. Please run the script again after logging in.');
    browser.disconnect();
    return;
  }

  // Navigate directly to the user's dashboard if not already there
  const targetDashboard = 'https://dev.shopify.com/dashboard/234984661';
  if (!page.url().includes('234984661')) {
    console.log(`Navigating to target dashboard: ${targetDashboard}`);
    await page.goto(targetDashboard, { waitUntil: 'networkidle2' });
  }

  await sleep(3000);
  await page.screenshot({ path: 'f:/Dropshipping/automation/step1_dashboard.png' });
  console.log('📸 Captured step1_dashboard.png');

  console.log('Current Dashboard Title:', await page.title());
  console.log('Current URL:', page.url());

  browser.disconnect();
  console.log('Bot monitor pass completed.');
}

runBot();
