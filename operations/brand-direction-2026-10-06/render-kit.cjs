const fs=require('node:fs');const path=require('node:path');
const sharp=require('C:/Users/Abhinand/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const dir=path.join(__dirname,'review-kit');
(async()=>{
  for(const name of ['IDENTITY-BOARD','MOBILE-CONCEPT','SHARE-CARD']) await sharp(path.join(dir,name+'.svg')).png().toFile(path.join(dir,name+'.png'));
  const logoNames=fs.readdirSync(path.join(dir,'logos')).filter(n=>n.endsWith('.svg'));
  for(const name of logoNames) await sharp(path.join(dir,'logos',name)).resize({width:name.includes('mark')&&!name.includes('wordmark')?512:1600}).png().toFile(path.join(dir,'logos',name.replace('.svg','.png')));
  for(const size of [16,32,180,192,512]) await sharp(path.join(dir,'logos','rozmiso-mark.svg')).resize(size,size).png().toFile(path.join(dir,'logos','favicon-'+size+'.png'));
  // Include a multi-size ICO for platforms that use it, sourced from the same SVG master.
  const sizes=[16,32,48];const pngs=[];
  for(const size of sizes) pngs.push(await sharp(path.join(dir,'logos','rozmiso-mark.svg')).resize(size,size).png().toBuffer());
  const header=Buffer.alloc(6+16*sizes.length);header.writeUInt16LE(1,2);header.writeUInt16LE(sizes.length,4);let offset=header.length;
  pngs.forEach((b,i)=>{const o=6+i*16;header[o]=sizes[i];header[o+1]=sizes[i];header.writeUInt16LE(1,o+4);header.writeUInt16LE(32,o+6);header.writeUInt32LE(b.length,o+8);header.writeUInt32LE(offset,o+12);offset+=b.length;});
  fs.writeFileSync(path.join(dir,'logos','favicon.ico'),Buffer.concat([header,...pngs]));
  console.log(JSON.stringify({rendered_boards:3,logo_exports:logoNames.length,favicon_sizes:sizes,live_deployment:false}));
})().catch(e=>{console.error(e);process.exitCode=1;});
