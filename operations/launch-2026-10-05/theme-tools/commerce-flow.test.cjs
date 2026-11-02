const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {JSDOM}=require('jsdom');
const source=fs.readFileSync('F:/Dropshipping/rozmiso-studio-theme/assets/studio.js','utf8');
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function setup(html,fetch){
 const dom=new JSDOM(html,{url:'https://example.test/en/collections/all',runScripts:'outside-only'});
 const w=dom.window;w.Shopify={routes:{root:'/en/'}};w.rozmisoLabels={searchAll:'View all results',searchMatches:'matching products',searchFailure:'Search unavailable',products:'products',cartError:'Open your full bag to verify the update.',adding:'Adding…'};w.fetch=fetch;
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};
 w.eval(source);return dom;
}
const searchFixture=`<template data-search-catalog><a href="/en/products/shaver" data-id="1" data-title="Actual fabric shaver" data-price="79900" data-available="false" data-keywords="fabric shaver"></a><a href="/en/products/brush" data-id="2" data-title="Actual cleaning brush" data-price="64900" data-available="false" data-keywords="cleaning brush"></a></template><div data-instant-search data-no-results="No products" data-loading="Searching" data-unavailable="Not available yet" data-currency="INR"><input data-search-input><div data-search-results hidden></div><span data-search-status></span></div>`;
test('stale indexed drafts are excluded and current availability/price wins',async()=>{
 let request;const dom=setup(searchFixture,async url=>{request=url;return {ok:true,json:async()=>({resources:{results:{products:[{id:99,title:'Unverified draft',price:10,available:true,url:'/products/draft'},{id:1,title:'Wrong indexed name',price:1,available:true,url:'/products/wrong'}]}}})};});
 const w=dom.window,input=w.document.querySelector('input');input.value='fabric';input.dispatchEvent(new w.Event('input',{bubbles:true}));await wait(260);
 const results=w.document.querySelector('[data-search-results]');assert.match(request,/^\/en\/search\/suggest\.json/);assert.match(results.textContent,/Actual fabric shaver/);assert.match(results.textContent,/799/);assert.match(results.textContent,/Not available yet/);assert.doesNotMatch(results.textContent,/Unverified draft|Wrong indexed name/);assert.equal(results.hidden,false);dom.window.close();
});
test('a late prior search response cannot overwrite the newer query',async()=>{
 const dom=setup(searchFixture,async url=>{const q=new URL(url,'https://example.test').searchParams.get('q');await wait(q==='fabric'?220:5);return {ok:true,json:async()=>({resources:{results:{products:[]}}})};});
 const w=dom.window,input=w.document.querySelector('input');input.value='fabric';input.dispatchEvent(new w.Event('input',{bubbles:true}));await wait(210);input.value='brush';input.dispatchEvent(new w.Event('input',{bubbles:true}));await wait(310);
 const results=w.document.querySelector('[data-search-results]');assert.match(results.textContent,/Actual cleaning brush/);assert.doesNotMatch(results.textContent,/Actual fabric shaver/);dom.window.close();
});
const cartFixture=`<a href="/en/cart" data-open-cart>Bag <span data-cart-badge>0</span></a><form id="ProductForm"><input type="hidden" name="id" value="123"><input type="number" name="quantity" value="1"><button data-add data-sold="Unavailable">Add to bag</button></form><dialog data-cart-dialog><button data-close-cart>Close</button><p hidden data-cart-error></p><div data-cart-content data-count="0">Empty</div></dialog>`;
test('rapid duplicate submissions send one add request and use server cart totals',async()=>{
 let posts=0;const dom=setup(cartFixture,async(url,options)=>{if(url.endsWith('cart/add.js')){posts++;assert.equal(options.body.get('id'),'123');await wait(25);return {ok:true,json:async()=>({id:123})};}return {ok:true,text:async()=>'<div data-cart-content data-count="1"><strong>Server discounted total ₹649</strong></div>'};});
 const w=dom.window,form=w.document.querySelector('form');form.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));const duplicate=new w.Event('submit',{bubbles:true,cancelable:true});form.dispatchEvent(duplicate);await wait(70);
 assert.equal(posts,1);assert.equal(duplicate.defaultPrevented,true);assert.equal(w.document.querySelector('dialog').open,true);assert.equal(w.document.querySelector('[data-cart-badge]').textContent,'1');assert.match(w.document.querySelector('[data-cart-content]').textContent,/Server discounted total ₹649/);assert.equal(form.querySelector('button').disabled,false);dom.window.close();
});
test('inventory rejection restores server quantity and does not retry the mutation',async()=>{
 let posts=0;const html=cartFixture.replace('data-count="0">Empty','data-count="1"><input data-cart-quantity data-key="123:line-key" type="number" min="0" value="1">');
 const dom=setup(html,async(url,options)=>{if(url.endsWith('cart/change.js')){posts++;assert.deepEqual(JSON.parse(options.body),{id:'123:line-key',quantity:2});return {ok:false,json:async()=>({description:'Only one unit is available'})};}return {ok:true,text:async()=>'<div data-cart-content data-count="1"><input data-cart-quantity data-key="123:line-key" type="number" min="0" value="1"></div>'};});
 const w=dom.window,input=w.document.querySelector('[data-cart-quantity]');input.value='2';input.dispatchEvent(new w.Event('change',{bubbles:true}));await wait(35);
 assert.equal(posts,1);assert.equal(w.document.querySelector('[data-cart-quantity]').value,'1');assert.equal(w.document.querySelector('[data-cart-quantity]').disabled,false);assert.equal(w.document.querySelector('[data-cart-error]').hidden,false);assert.match(w.document.querySelector('[data-cart-error]').textContent,/Only one unit/);dom.window.close();
});
