const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function main() {
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const tab = (await browser.pages())[0];

  console.log('Checking frames...');
  for (let i = 0; i < tab.frames().length; i++) {
    const f = tab.frames()[i];
    const matches = await f.evaluate(() => {
      const all = Array.from(document.querySelectorAll('*'));
      return all.filter(el => /import/i.test(el.textContent || '') && el.children.length <= 2)
        .map(el => ({
          tag: el.tagName,
          text: el.textContent.trim(),
          rect: el.getBoundingClientRect()
        }));
    }).catch(() => []);
    if (matches.length > 0) {
      console.log(`Frame ${i} (${f.url().substring(0, 50)}) matches:`, matches);
    }
  }

  browser.disconnect();
}

main().catch(console.error);
