const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function doThemeUpload() {
  console.log('Connecting to Chrome...');
  const devToolsPath = 'C:\\Users\\Abhinand\\AppData\\Local\\Google\\Chrome\\User Data\\DevToolsActivePort';
  const content = fs.readFileSync(devToolsPath, 'utf8').trim().split(/\r?\n/);
  const wsEndpoint = 'ws://127.0.0.1:' + content[0] + content[1];

  const browser = await puppeteer.connect({ browserWSEndpoint: wsEndpoint, defaultViewport: null });
  const pages = await browser.pages();
  let themePage = pages.find(p => p.url().includes('0ghddv-sg/themes') && !p.url().includes('themes/'));

  console.log('Page:', await themePage.title());

  // Click the "Import" button
  console.log('Looking for Import button...');
  const clickedImport = await themePage.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, a'));
    const importBtn = btns.find(b => b.innerText && b.innerText.trim().toLowerCase().startsWith('import'));
    if (importBtn) {
      importBtn.click();
      return true;
    }
    return false;
  });

  console.log('Clicked import button:', clickedImport);
  await sleep(1500);

  // Take screenshot of opened dropdown/dialog
  await themePage.screenshot({ path: 'f:/Dropshipping/automation/themes_after_import_click.png' });
  console.log('Saved screenshot to themes_after_import_click.png');

  // Find any file input or modal options
  const pageState = await themePage.evaluate(() => {
    const fileInputs = Array.from(document.querySelectorAll('input[type="file"]')).map(i => ({
      name: i.name,
      id: i.id,
      accept: i.accept
    }));
    const visibleTexts = Array.from(document.querySelectorAll('[role="menuitem"], [role="option"], button, a'))
      .map(e => e.innerText ? e.innerText.trim() : '')
      .filter(t => t.length > 0 && t.length < 50);

    return { fileInputs, visibleTexts };
  });

  console.log('Page state:', JSON.stringify(pageState, null, 2));

  // If there's a menuitem like "Upload zip file", click it
  const clickedUploadZip = await themePage.evaluate(() => {
    const items = Array.from(document.querySelectorAll('[role="menuitem"], button, a, span'));
    const zipItem = items.find(i => i.innerText && /upload (zip|file|theme)/i.test(i.innerText.trim()));
    if (zipItem) {
      zipItem.click();
      return zipItem.innerText.trim();
    }
    return null;
  });

  console.log('Clicked upload zip option:', clickedUploadZip);
  await sleep(2000);

  await themePage.screenshot({ path: 'f:/Dropshipping/automation/themes_modal.png' });
  console.log('Saved screenshot to themes_modal.png');

  // Check for file input in modal
  const fileInputHandle = await themePage.$('input[type="file"]');
  if (fileInputHandle) {
    console.log('Found file input! Uploading rozmiso-theme.zip...');
    const zipPath = path.resolve('f:/Dropshipping/rozmiso-shopify-store/rozmiso-theme.zip');
    await fileInputHandle.uploadFile(zipPath);
    console.log('File attached to input!');
    await sleep(2000);
    await themePage.screenshot({ path: 'f:/Dropshipping/automation/themes_file_attached.png' });

    // Look for submit / Upload button in modal
    const submitted = await themePage.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const uploadBtn = btns.find(b => b.innerText && /upload/i.test(b.innerText.trim()) && !b.disabled);
      if (uploadBtn) {
        uploadBtn.click();
        return uploadBtn.innerText.trim();
      }
      return null;
    });

    console.log('Submitted upload:', submitted);
    await sleep(5000);
    await themePage.screenshot({ path: 'f:/Dropshipping/automation/themes_after_upload.png' });
  } else {
    console.log('No file input found yet.');
  }

  browser.disconnect();
}

doThemeUpload().catch(e => console.error('Error:', e));
