const fs=require('fs'),path=require('path');
const root='F:/Dropshipping/rozmiso-studio-theme';
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const write=(p,s)=>fs.writeFileSync(path.join(root,p),s);
const index=JSON.parse(read('templates/index.json'));
const catalog=JSON.parse(fs.readFileSync('F:/Dropshipping/operations/launch-2026-10-05/catalog.json','utf8'));
const storefrontHandles=['usb-rechargeable-fabric-shaver','5-in-1-rechargeable-cleaning-brush','everyday-travel-organizer-pouch','2-in-1-soap-dispensing-cleaning-brush'];
catalog.forEach((p,i)=>{index.sections.edit.blocks['item'+i].settings.product=storefrontHandles[i];});
index.sections.hero.settings.button_label='Shop the collection';
index.sections.edit.settings.heading='Find your everyday essential.';
write('templates/index.json',JSON.stringify(index,null,2));
let edit=read('sections/studio-edit.liquid');
edit=edit.replace('<article class="product-card" {{ block.shopify_attributes }}>','<div {{ block.shopify_attributes }}>').replace('{% endif %}</article>{% endfor %}','{% endif %}</div>{% endfor %}');
write('sections/studio-edit.liquid',edit);
const locale=JSON.parse(read('locales/en.default.json'));
Object.assign(locale.product,{sold_out:'Not available yet',availability_contact:'Ask about availability',view:'View product',catalog_title:'Shop everyday essentials',catalog_description:'Practical finds for your home, kitchen and days away. Explore the details and choose what fits your routine.',categories:'Filter by category',all:'All products'});
write('locales/en.default.json',JSON.stringify(locale,null,2));
const css=`\n/* Shopping catalog refinement */
.shop-catalog{padding-top:32px;padding-bottom:72px;min-height:60vh}.shop-catalog .breadcrumb{margin-bottom:24px}.catalog-heading{display:flex;justify-content:space-between;align-items:end;gap:48px}.catalog-heading h1{font-size:clamp(32px,3.4vw,48px);letter-spacing:-.045em;margin-top:10px}.catalog-heading>p{max-width:390px;color:var(--muted);font-size:14px}.shop-catalog .collection-toolbar{margin:26px 0 18px;padding-bottom:18px;border-bottom:1px solid var(--line)}.category-filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px}.category-filter{border:1px solid var(--line);border-radius:24px;padding:9px 18px;background:transparent;font-size:13px}.category-filter[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:white}.product-card{background:#fff;border:1px solid var(--line);height:100%;overflow:hidden}.product-card .card-image{border-bottom:1px solid var(--line);background:#f1f2ec}.product-card .card-meta{padding:18px}.product-card h3{min-height:48px}.product-card .card-price{font-size:20px;font-weight:600;margin:12px 0}.card-shop-link{display:flex;justify-content:space-between;align-items:center;border:1px solid var(--ink);padding:11px 14px;font-size:13px;font-weight:600;margin-top:16px}.card-shop-link:hover{background:var(--ink);color:white;text-decoration:none}.product-card .pill{font-size:10px;padding:5px 9px}.catalog-empty{grid-column:1/-1;padding:36px;background:var(--sage)}.catalog-empty h2{font-size:24px;margin-bottom:20px}@media(max-width:700px){.shop-catalog{padding-top:24px;padding-bottom:44px}.catalog-heading{display:block}.catalog-heading>p{margin-top:14px}.shop-catalog .collection-toolbar{gap:12px;flex-wrap:wrap}.product-card .card-meta{padding:12px}.product-card h3{font-size:14px;min-height:58px}.product-card .card-price{font-size:18px}.card-shop-link{padding:9px;font-size:12px}.product-card .pill{left:7px;top:7px;font-size:9px}.category-filter{padding:8px 13px;font-size:12px}}\n`;
if(!read('assets/studio.css').includes('Shopping catalog refinement'))write('assets/studio.css',read('assets/studio.css')+css);
const js=`\n// Progressive enhancement: categories and sorting retain native links/forms.
document.querySelectorAll('[data-category-filters]').forEach(el=>el.hidden=false);
document.addEventListener('change',event=>{if(event.target.matches('[data-auto-sort]'))event.target.form.requestSubmit();});
document.addEventListener('click',event=>{const button=event.target.closest('[data-filter]');if(!button)return;const root=button.closest('[data-catalog]');root.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;root.querySelectorAll('[data-catalog-grid] .product-card').forEach(card=>{const show=button.dataset.filter==='all'||card.dataset.category===button.dataset.filter;card.hidden=!show;if(show)count++;});root.querySelector('[data-result-count]').textContent=count+' products';});\n`;
if(!read('assets/studio.js').includes('Progressive enhancement: categories'))write('assets/studio.js',read('assets/studio.js')+js);
fs.writeFileSync('F:/Dropshipping/operations/launch-2026-10-05/shopping-change-files.json',JSON.stringify(['snippets/studio-card.liquid','sections/studio-collection.liquid','sections/studio-edit.liquid','templates/index.json','locales/en.default.json','assets/studio.css','assets/studio.js']));
