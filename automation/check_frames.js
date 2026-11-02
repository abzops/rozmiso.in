const puppeteer = require('puppeteer-core');
const fs = require('fs');

function log(msg) {
  fs.appendFileSync('f:/Dropshipping/automation/bot.log', msg + '\n');
}

async function main() {
  fs.writeFileSync('f:/Dropshipping/automation/bot.log', 'Inspecting all frames...\n');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:' + content[0] + content[1], defaultViewport: null });
  const page = (await browser.pages()).find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));

  const frames = page.frames();
  log(`Total frames: ${frames.length}`);

  for (let i = 0; i < frames.length; i++) {
    const f = frames[i];
    log(`Frame ${i}: ${f.url()}`);
    try {
      const texts = await f.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a'));
        return btns.map(b => b.innerText ? b.innerText.trim() : '').filter(t => t.length > 0);
      });
      log(`Frame ${i} buttons: ${JSON.stringify(texts.slice(0, 15))}`);
    } catch (e) {
      log(`Frame ${i} eval failed: ${e.message}`);
    }
  }

  browser.disconnect();
}

main().catch(e => log('Error: ' + e.message));
