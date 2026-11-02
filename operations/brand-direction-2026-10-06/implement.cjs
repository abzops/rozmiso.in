const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..'),source=path.join(root,'rozmiso-studio-theme'),target=path.join(__dirname,'theme-approved'),backup=path.join(__dirname,'theme-before-approved');
if(!fs.existsSync(backup))fs.cpSync(source,backup,{recursive:true});
fs.cpSync(backup,target,{recursive:true});
const read=f=>fs.readFileSync(path.join(target,f),'utf8'),write=(f,s)=>fs.writeFileSync(path.join(target,f),s);
const kit=path.join(__dirname,'review-kit');
for(const n of ['rozmiso-primary.svg','rozmiso-primary-reversed.svg','rozmiso-mark.svg','favicon-16.png','favicon-32.png','favicon-180.png','favicon.ico'])fs.copyFileSync(path.join(kit,'logos',n),path.join(target,'assets',n));
fs.copyFileSync(path.join(kit,'SHARE-CARD.png'),path.join(target,'assets','rozmiso-share.png'));
for(const name of ['Manrope-Variable.ttf','DMSans-Variable.ttf'])fs.copyFileSync(path.join(__dirname,'fonts',name),path.join(target,'assets',name));
fs.copyFileSync(path.join(__dirname,'fonts','OFL.txt'),path.join(target,'assets','Manrope-OFL.txt'));
fs.copyFileSync(path.join(__dirname,'fonts','DM-Sans-OFL.txt'),path.join(target,'assets','DM-Sans-OFL.txt'));
let icons='{% doc %}\nRenders a decorative interface icon.\n@param {string} name - Icon name\n{% enddoc %}\n<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{% case name %}';
for(const name of ['search','bag','menu','close','arrow-right','chevron-down','plus','minus','home','support','filter','mail']){let s=fs.readFileSync(path.join(kit,'icons',name+'.svg'),'utf8');icons+=`{% when '${name}' %}`+s.match(/<g[^>]*>([\s\S]*?)<\/g>/)[1];}
icons+='{% endcase %}</g></svg>\n';write('snippets/studio-icon.liquid',icons);
write('snippets/studio-logo.liquid',`{% doc %}\nRenders the approved Rozmiso logo.\n@param {boolean} [reversed] - Use the light logo\n{% enddoc %}\n{% if reversed %}{% assign logo_asset = 'rozmiso-primary-reversed.svg' %}{% else %}{% assign logo_asset = 'rozmiso-primary.svg' %}{% endif %}\n<img class="brand-logo" src="{{ logo_asset | asset_url }}" alt="{{ shop.name | escape }}" width="454" height="120">\n`);
let header=read('sections/studio-header.liquid');
header=header.replace(/<svg class="brand-mark"[\s\S]*?<\/svg><span class="brand-name">[\s\S]*?<\/span><\/span>/,"{% render 'studio-logo' %}");
header=header.replace(/<svg viewBox="0 0 24 24"[\s\S]*?<\/svg>/g,(s)=>"{% render 'studio-icon', name: '"+(s.includes('circle')?'search':s.includes('M5 7')?'bag':s.includes('M3 6')?'menu':'arrow-right')+"' %}");
header=header.replace(/<a class="mobile-search-link"[\s\S]*?<\/a>/,'').replace(/<a class="support-tab"[\s\S]*?<\/a>/,'');
header=header.replace('data-close-cart>×','data-close-cart>{% render \'studio-icon\', name: \'close\' %}');
// Native details remains the mobile disclosure; functional cart/search hooks remain intact.
header=header.replace(/<nav><a /,'<nav aria-label="{{ \'general.navigation\' | t }}"><a ');
write('sections/studio-header.liquid',header);
const heroSchema=read('sections/studio-hero.liquid').split('{% schema %}')[1];
write('sections/studio-hero.liquid',`{% assign featured = all_products['usb-rechargeable-fabric-shaver'] %}
<nav class="category-strip shell" aria-label="{{ 'home.browse_categories' | t }}" id="home-categories">
{% assign category_handles = 'home-care,kitchen-essentials,travel-essentials' | split: ',' %}
{% for handle in category_handles %}{% assign category = collections[handle] %}{% if category != blank %}<a href="{{ category.url }}">{% case handle %}{% when 'home-care' %}{{ 'general.home_care' | t }}{% when 'kitchen-essentials' %}{{ 'general.kitchen' | t }}{% when 'travel-essentials' %}{{ 'general.travel' | t }}{% endcase %}</a>{% endif %}{% endfor %}
</nav>
<section class="hero shell" aria-labelledby="FeaturedHeading">
<div class="hero-copy"><p class="eyebrow hero-kicker">{{ section.settings.eyebrow | escape }}</p><h1 id="FeaturedHeading">{{ section.settings.heading | escape }}</h1><p class="hero-description">{{ section.settings.description | escape }}</p></div>
<a class="hero-art" href="{% if featured != blank %}{{ featured.url }}{% else %}{{ routes.all_products_collection_url }}{% endif %}" aria-label="{{ featured.title | default: section.settings.image_alt | escape }}">
{% if featured.featured_image %}{{ featured.featured_image | image_url: width: 1100 | image_tag: widths: '400, 700, 1100', sizes: '(min-width: 900px) 45vw, 100vw', loading: 'eager', fetchpriority: 'high', class: 'hero-photo', alt: featured.title }}{% elsif section.settings.image %}{{ section.settings.image | image_url: width: 1100 | image_tag: widths: '400, 700, 1100', sizes: '(min-width: 900px) 45vw, 100vw', loading: 'eager', fetchpriority: 'high', class: 'hero-photo' }}{% elsif section.settings.image_url != blank %}<img class="hero-photo" src="{{ section.settings.image_url | escape }}" width="1000" height="1000" alt="{{ section.settings.image_alt | escape }}" fetchpriority="high">{% endif %}</a>
<div class="hero-detail">{% if featured != blank %}<a class="featured-title" href="{{ featured.url }}">{{ featured.title | escape }}</a><p class="spotlight-price"><strong>{{ featured.price | money }}</strong>{% unless featured.available %}<span>{{ 'product.sold_out' | t }}</span>{% endunless %}</p>{% endif %}<a class="button wide" href="{{ routes.all_products_collection_url }}">{{ section.settings.button_label | escape }} {% render 'studio-icon', name: 'arrow-right' %}</a></div>
</section>
{% schema %}`+heroSchema);
let card=read('snippets/studio-card.liquid');
card=card.replace(/{% unless item.available %}<span class="pill">[\s\S]*?<\/span>{% endunless %}/,'');
card=card.replace('</p><a class="card-shop-link"','</p>{% unless item.available %}<p class="card-availability">{{ \'product.sold_out\' | t }}</p>{% endunless %}<a class="card-shop-link"');
card=card.replace('<span aria-hidden="true">→</span>',"{% render 'studio-icon', name: 'arrow-right' %}");
write('snippets/studio-card.liquid',card);
let edit=read('sections/studio-edit.liquid');
edit=edit.replace(/<a class="text-link edit-all"[\s\S]*?<\/a>/,'');
edit=edit.replace('<p class="eyebrow">{{ section.settings.eyebrow | escape }}</p>','');
write('sections/studio-edit.liquid',edit);
let footer=read('sections/studio-footer.liquid');
footer=footer.replace(/<div class="footer-brand-line">[\s\S]*?<\/div>/,'');
footer=footer.replace(/<svg class="brand-mark"[\s\S]*?<\/svg><span class="brand-name">[\s\S]*?<\/span><\/span>/,"{% render 'studio-logo', reversed: true %}");
footer=footer.replace('<p>{{ settings.brand_description | escape }}</p>','<p>{{ settings.brand_description | escape }}</p>');
write('sections/studio-footer.liquid',footer);
let story=read('sections/studio-story.liquid');
story=story.replace(/<div class="story-emblem">[\s\S]*?<\/div><p class="story-signature">[\s\S]*?<\/p>/,'');
story=story.replace(/<div class="story-values">[\s\S]*?<\/div><\/div><\/div><\/div>/,'</div></div>');
write('sections/studio-story.liquid',story);
let index=JSON.parse(read('templates/index.json'));
Object.assign(index.sections.hero.settings,{eyebrow:'THE HOME CARE EDIT',heading:'A fresh start for\nyour favourite fabrics.',description:'Explore a compact fabric shaver, alongside practical finds for home and travel.',button_label:'Explore the collection'});
Object.assign(index.sections.edit.settings,{eyebrow:'EXPLORE ROZMISO',heading:'Everyday essentials',description:''});
index.sections.edit.block_order=['item1','item2','item3','item0'].filter(k=>index.sections.edit.blocks[k]);
// Keep the original block IDs if an existing installation uses another naming convention.
if(index.sections.edit.block_order.length!==4)index.sections.edit.block_order=Object.keys(index.sections.edit.blocks);
Object.assign(index.sections.story.settings,{eyebrow:'OUR APPROACH',heading:'Useful things, clearly explained.',body:'Explore product details, care guidance and prices in one place. Our first collection is being prepared; ordering is not available yet.'});
write('templates/index.json',JSON.stringify(index,null,2)+'\n');
let config=JSON.parse(read('config/settings_data.json'));config.current.prelaunch_mode=true;config.current.brand_description='Practical finds for home care, kitchen routines and travel.';write('config/settings_data.json',JSON.stringify(config,null,2)+'\n');
let locale=JSON.parse(read('locales/en.default.json'));locale.general.launch_notice='Collection preview · Orders are not open yet';locale.general.search_short='Search the collection';locale.home.footer_note='Home care. Kitchen. Travel.';write('locales/en.default.json',JSON.stringify(locale,null,2)+'\n');
let layout=read('layout/theme.liquid');
layout=layout.replace(/{% if settings.favicon != blank %}[\s\S]*?{% endif %}/,`{% if settings.favicon != blank %}<link rel="icon" type="image/png" sizes="32x32" href="{{ settings.favicon | image_url: width: 32, height: 32 }}"><link rel="apple-touch-icon" sizes="180x180" href="{{ settings.favicon | image_url: width: 180, height: 180 }}">{% else %}<link rel="icon" type="image/png" sizes="16x16" href="{{ 'favicon-16.png' | asset_url }}"><link rel="icon" type="image/png" sizes="32x32" href="{{ 'favicon-32.png' | asset_url }}"><link rel="icon" type="image/svg+xml" sizes="any" href="{{ 'rozmiso-mark.svg' | asset_url }}"><link rel="apple-touch-icon" sizes="180x180" href="{{ 'favicon-180.png' | asset_url }}">{% endif %}`);
layout=layout.replace(/{% if page_image %}<meta property="og:image"[\s\S]*?{% endif %}/,`{% if page_image %}{% assign share_image = page_image | image_url: width: 1200 | prepend: 'https:' %}{% else %}{% assign share_image = 'rozmiso-share.png' | asset_url | prepend: 'https:' %}{% endif %}<meta property="og:image" content="{{ share_image }}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{{ share_image }}">`);
layout=layout.replace("{{ content_for_header }}",`<style>@font-face{font-family:'DM Sans';src:url({{ 'DMSans-Variable.ttf' | asset_url }}) format('truetype');font-weight:100 1000;font-display:swap}@font-face{font-family:'Manrope';src:url({{ 'Manrope-Variable.ttf' | asset_url }}) format('truetype');font-weight:200 800;font-display:swap}</style>\n{{ content_for_header }}`);
write('layout/theme.liquid',layout);
// Preserve product, catalog, cart and enquiry rules; replace the accumulated homepage/header overrides.
const old=fs.readFileSync(path.join(backup,'assets/studio.css'),'utf8');
const base=old.split('\n')[1];
let retained=base.slice(base.indexOf('.breadcrumb{'));
const commerce=old.slice(old.indexOf('.catalog-refinements{'),old.indexOf('@media(min-width:1001px)',old.indexOf('.catalog-refinements{')));
const launch=old.slice(old.indexOf('.shaver-intro{'),old.indexOf('/* Rozmiso brand refinement'));
write('assets/studio.css',fs.readFileSync(path.join(__dirname,'approved.css'),'utf8')+'\n/* Preserved commerce and product behavior */\n'+retained+'\n'+commerce+'\n'+launch+'\n'+fs.readFileSync(path.join(__dirname,'responsive.css'),'utf8'));
const boardPath=path.join(root,'team/TASK-BOARD.json'),board=JSON.parse(fs.readFileSync(boardPath,'utf8'));
board.tasks.find(t=>t.id==='T010').owner_visual_review='APPROVED';
let t=board.tasks.find(t=>t.id==='T011');Object.assign(t,{status:'IN_PROGRESS',blockers:[],inputs:['operations/brand-direction-2026-10-06/review-kit','rozmiso-studio-theme'],allowed_actions:['Implement the CEO-approved brand/mobile direction locally; validate and upload a draft theme; visually verify and deploy the authorized design. No commerce launch, inventory, payment, spending or identity changes.'],allowed_write_paths:['operations/brand-direction-2026-10-06/theme-approved/**','rozmiso-studio-theme/**','team/reports/T011/**'],execution_evidence:{started_at:new Date().toISOString(),author:'Codex',owner_approval:'All are approved.',rollback:'operations/brand-direction-2026-10-06/theme-before-approved'}});
fs.writeFileSync(boardPath,JSON.stringify(board,null,2)+'\n');
console.log(JSON.stringify({theme:target,backup,files:fs.readdirSync(path.join(target,'assets')).length}));
