const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const deps='F:/Dropshipping/operations/launch-2026-10-05/theme-tools/node_modules';
const {Liquid}=require(path.join(deps,'liquidjs'));
const {JSDOM}=require(path.join(deps,'jsdom'));
const engine=new Liquid();
engine.registerFilter('asset_url',s=>'/assets/'+s);
engine.registerFilter('money',n=>'INR '+(n/100).toFixed(2));
const template=fs.readFileSync('rozmiso-studio-theme/sections/studio-landing.liquid','utf8').replace(/{% schema %}[\s\S]*?{% endschema %}/,'').replace(/{% render [\s\S]*?%}/g,'<svg aria-hidden="true"></svg>');
const handles=['2-in-1-soap-dispensing-cleaning-brush','3-in-1-bottle-lid-cleaning-tool','5-in-1-rechargeable-cleaning-brush','adhesive-cable-organizer-clips-set-of-20'];
function context(guard=true){return {routes:{all_products_collection_url:'/collections/all',root_url:'/'},settings:{prelaunch_mode:guard},collections:{'home-care':{url:'/collections/home-care'},'kitchen-essentials':{url:'/collections/kitchen-essentials'},'travel-essentials':{url:'/collections/travel-essentials'}},all_products:Object.fromEntries(handles.map((h,i)=>[h,{title:'Verified Product '+i,url:'/products/'+h,price:12345+i,available:true}]))};}
test('landing renders all reference sections and native product fixture prices/links',async()=>{const html=await engine.parseAndRender(template,context());const d=new JSDOM(html).window.document;assert.equal(d.querySelectorAll('h1').length,1);assert.equal(d.querySelectorAll('.rl-category').length,5);assert.equal(d.querySelectorAll('.rl-product').length,4);assert.equal(d.querySelector('.rl-price').textContent,'INR 123.45');assert.equal(d.querySelector('.rl-product h3 a').getAttribute('href'),'/products/'+handles[0]);assert.equal(d.querySelector('.rl-hero-image').getAttribute('fetchpriority'),'high');assert.equal(d.querySelectorAll('.rl-benefit').length,4);assert.equal(d.querySelectorAll('.rl-home-banner,.rl-travel-banner').length,2);assert.doesNotMatch(html,/4\.8|\(320\)|Pan India|most loved|reviewCount|aggregateRating/);});
test('commerce guard and actual availability drive factual card copy',async()=>{const guarded=await engine.parseAndRender(template,context());assert.equal((guarded.match(/Currently unavailable/g)||[]).length,4);const c=context(false);c.all_products[handles[1]].available=false;const normal=await engine.parseAndRender(template,c);assert.equal((normal.match(/Currently unavailable/g)||[]).length,1);assert.equal((normal.match(/View product details/g)||[]).length,3);assert.doesNotMatch(normal,/<form/);});
test('missing products are omitted without fabricated prices and missing category has safe destination',async()=>{const c=context();delete c.all_products[handles[1]];c.collections={};const html=await engine.parseAndRender(template,c);const d=new JSDOM(html).window.document;assert.equal(d.querySelectorAll('.rl-product').length,3);assert.equal(d.querySelector('.rl-category').getAttribute('href'),'/collections/all');});
