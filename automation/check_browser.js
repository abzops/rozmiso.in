const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  if (!fs.existsSync(devToolsPath)) {
    console.log('DevToolsActivePort does not exist');
    return;
  }

  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const port = content[0];
  const wsPath = content[1];
  const wsEndpoint = `ws://127.0.0.1:${port}${wsPath}`;
  console.log('Connecting to browser at:', wsEndpoint);

  try {
    const browser = await puppeteer.connect({
      browserWSEndpoint: wsEndpoint,
      defaultViewport: null
    });

    console.log('Successfully connected to browser!');
    const pages = await browser.pages();
    console.log(`Found ${pages.length} open pages:`);
    for (let i = 0; i < pages.length; i++) {
      const title = await pages[i].title();
      const url = pages[i].url();
      console.log(`[${i}] Title: "${title}" | URL: "${url}"`);
    }

    browser.disconnect();
  } catch (err) {
    console.error('Connection failed:', err.message);
  }
}

main();
