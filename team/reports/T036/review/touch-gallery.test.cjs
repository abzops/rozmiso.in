const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM} = require('F:/Dropshipping/operations/launch-2026-10-05/theme-tools/node_modules/jsdom');
const sourcePath = path.resolve('rozmiso-studio-theme/assets/studio.js');

function fixture(count=3, bento=false) {
  const buttons = Array.from({length:count}, (_,i) => `<button data-image="/image-${i}.jpg" data-image-id="image-${i}" data-alt="Product angle ${i}" aria-pressed="${i===0}"><img alt="" src="/thumb-${i}.jpg"></button>`).join('');
  const dom = new JSDOM(`<body data-prelaunch="true"><section data-product><div class="${bento?'bento-gallery ':''}gallery"><div class="${bento?'bento-main-photo ':''}main-photo" data-zoom-image role="button" tabindex="0"><img id="ProductImage" src="/image-0.jpg" srcset="/image-0.jpg 600w" alt="Product angle 0"></div><div class="thumbs">${buttons}</div></div></section><dialog data-image-dialog><img data-zoom-target><button data-close-image></button></dialog></body>`, {url:'https://rozmiso.myshopify.com/products/sample', runScripts:'outside-only'});
  const w=dom.window, d=w.document;
  w.PointerEvent=class PointerEvent extends w.MouseEvent { constructor(type,init={}) {super(type,init);Object.defineProperties(this,{pointerId:{value:init.pointerId??1},pointerType:{value:init.pointerType??'touch'},isPrimary:{value:init.isPrimary??true}});} };
  const surface=d.querySelector('[data-zoom-image]');
  surface.getBoundingClientRect=()=>({width:390,height:390,left:0,top:0,right:390,bottom:390});
  Object.defineProperty(surface,'clientWidth',{value:390});
  surface.setPointerCapture=()=>{};surface.releasePointerCapture=()=>{};
  const dialog=d.querySelector('dialog');let opened=0;
  dialog.showModal=()=>{opened++;dialog.open=true;};dialog.close=()=>{dialog.open=false;};
  w.eval(fs.readFileSync(sourcePath,'utf8'));
  const pointer=(type,x,y,extra={})=>{const event=new w.PointerEvent(type,{bubbles:true,cancelable:true,clientX:x,clientY:y,button:0,buttons:type==='pointerup'?0:1,...extra});surface.dispatchEvent(event);return event;};
  const click=(detail=1)=>{const event=new w.MouseEvent('click',{bubbles:true,cancelable:true,detail});surface.querySelector('img').dispatchEvent(event);return event;};
  const swipe=(dx=-140,dy=0,extra={})=>{pointer('pointerdown',200,180,extra);pointer('pointermove',200+dx,180+dy,extra);pointer('pointerup',200+dx,180+dy,extra);};
  const index=()=>[...d.querySelectorAll('button[data-image]')].findIndex(b=>b.getAttribute('aria-pressed')==='true');
  return {dom,w,d,surface,pointer,click,swipe,index,opened:()=>opened};
}

for(const bento of [false,true]) {
  const label=bento?'Bento':'native';
  test(`${label}: horizontal swipe selects the next thumbnail and synchronizes source, alt and aria`,()=>{
    const f=fixture(3,bento);f.swipe();assert.equal(f.index(),1);assert.equal(f.d.querySelector('#ProductImage').getAttribute('src'),'/image-1.jpg');assert.equal(f.d.querySelector('#ProductImage').alt,'Product angle 1');assert.equal(f.d.querySelector('#ProductImage').hasAttribute('srcset'),false);assert.equal(f.opened(),0);f.dom.window.close();
  });
  test(`${label}: swipe right/left wraps first and last and never skips an image`,()=>{
    const f=fixture(3,bento);f.swipe(140);assert.equal(f.index(),2);f.swipe(-140);assert.equal(f.index(),0);f.swipe(-140);assert.equal(f.index(),1);f.dom.window.close();
  });
}

test('real touch tap retains zoom and keyboard Enter/Space remain usable',()=>{
  const f=fixture();f.pointer('pointerdown',180,180);f.pointer('pointerup',184,181);f.click();assert.equal(f.opened(),1);assert.equal(f.index(),0);for(const key of ['Enter',' ']) f.surface.dispatchEvent(new f.w.KeyboardEvent('keydown',{bubbles:true,cancelable:true,key}));assert.equal(f.opened(),3);f.dom.window.close();
});
test('synthetic click after swipe is suppressed rather than opening zoom',()=>{
  const f=fixture();f.swipe();const click=f.click();assert.equal(f.index(),1);assert.equal(f.opened(),0);assert.equal(click.defaultPrevented,true);f.dom.window.close();
});
test('vertical, diagonal and short movements leave gallery and native page gesture untouched',()=>{
  for(const [dx,dy] of [[0,160],[50,160],[140,140],[-20,0]]) {
    const f=fixture();f.pointer('pointerdown',200,180);const move=f.pointer('pointermove',200+dx,180+dy);f.pointer('pointerup',200+dx,180+dy);assert.equal(f.index(),0,`${dx},${dy}`);assert.equal(move.defaultPrevented,false);f.dom.window.close();
  }
});
test('mouse drags do not select gallery photos or alter click zoom',()=>{
  const f=fixture();f.swipe(-150,0,{pointerType:'mouse'});assert.equal(f.index(),0);f.click();assert.equal(f.opened(),1);f.dom.window.close();
});
test('pen swipe uses the same gallery path',()=>{
  const f=fixture();f.swipe(-150,0,{pointerType:'pen'});assert.equal(f.index(),1);f.dom.window.close();
});
test('pointer cancellation never selects an image and the next fresh gesture works',()=>{
  const f=fixture();f.pointer('pointerdown',200,180);f.pointer('pointermove',50,180);f.pointer('pointercancel',50,180);f.pointer('pointerup',50,180);assert.equal(f.index(),0);f.swipe();assert.equal(f.index(),1);f.dom.window.close();
});
test('a second touch cancels the gesture even if the first pointer finishes with a large displacement',()=>{
  const f=fixture();f.pointer('pointerdown',200,180,{pointerId:1});f.pointer('pointerdown',250,180,{pointerId:2,isPrimary:false});f.pointer('pointermove',40,180,{pointerId:1});f.pointer('pointerup',40,180,{pointerId:1});f.pointer('pointerup',250,180,{pointerId:2,isPrimary:false});assert.equal(f.index(),0);f.swipe();assert.equal(f.index(),1);f.dom.window.close();
});
test('zero or one thumbnail is safe and never interferes with tap zoom',()=>{
  for(const count of [0,1]) {const f=fixture(count);f.swipe();assert.equal(f.index(),count?0:-1);f.click();assert.equal(f.opened(),1);f.dom.window.close();}
});
test('thumbnail clicks remain usable before and after swiping',()=>{
  const f=fixture();f.d.querySelectorAll('button[data-image]')[2].click();assert.equal(f.index(),2);f.swipe();assert.equal(f.index(),0);f.d.querySelectorAll('button[data-image]')[1].click();assert.equal(f.index(),1);f.dom.window.close();
});
test('a deliberate new tap immediately after a swipe still opens the chosen image',()=>{
  const f=fixture();f.swipe();f.click();assert.equal(f.opened(),0);f.pointer('pointerdown',180,180);f.pointer('pointerup',182,180);f.click();assert.equal(f.opened(),1);assert.equal(f.d.querySelector('[data-zoom-target]').alt,'Product angle 1');f.dom.window.close();
});
test('a second touch does not allow accidental click-to-zoom on gesture completion',()=>{
  const f=fixture();f.pointer('pointerdown',180,180,{pointerId:1});f.pointer('pointerdown',210,180,{pointerId:2,isPrimary:false});f.pointer('pointerup',180,180,{pointerId:1});f.pointer('pointerup',210,180,{pointerId:2,isPrimary:false});f.click();assert.equal(f.opened(),0);f.dom.window.close();
});
