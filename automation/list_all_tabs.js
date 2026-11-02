const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const pages = await browser.pages();

  console.log(`Total tabs open: ${pages.length}`);
  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    console.log(`\n--- Tab [${i}]: "${await p.title()}" ---`);
    console.log(`URL: ${p.url()}`);
    const frames = p.frames();
    console.log(`Frames (${frames.length}):`);
    frames.forEach((f, idx) => console.log(`  [${idx}] ${f.url()}`));
  }

  browser.disconnect();
}

main().catch(e => console.error(e));
