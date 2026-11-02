const fs=require('node:fs');
const path=require('node:path');
const sharp=require('C:/Users/Abhinand/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const dir='F:/Dropshipping/operations/brand-2026-10-06';
const svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#26342e"/><path fill="#fbfaf6" fill-rule="evenodd" d="M9 7h8a7 7 0 0 1 0 14h-3v5H9V7Zm5 5v4h3a2 2 0 0 0 0-4h-3Z"/><path fill="#fbfaf6" d="m17 18 8 8h-7l-6-7Z"/></svg>';
fs.writeFileSync(path.join(dir,'rozmiso-mark.svg'),svg);
(async()=>{for(const size of [16,32,180,512]) await sharp(Buffer.from(svg)).resize(size,size).png().toFile(path.join(dir,`rozmiso-brand-${size}.png`)); console.log('Created one SVG master and 16/32/180/512px matching PNGs.');})();
