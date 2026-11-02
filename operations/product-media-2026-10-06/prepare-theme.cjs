const fs=require('node:fs'),path=require('node:path');
const op=__dirname,live=path.resolve(op,'../../rozmiso-studio-theme'),theme=path.join(op,'theme-prepared'),backup=path.join(op,'theme-before');
for(const folder of ['assets','config','layout','locales','sections','snippets','templates']){
 if(!fs.existsSync(path.join(backup,folder)))fs.cpSync(path.join(live,folder),path.join(backup,folder),{recursive:true});
 fs.cpSync(path.join(backup,folder),path.join(theme,folder),{recursive:true});
}
const file=(name)=>path.join(theme,name);
let hero=fs.readFileSync(file('sections/studio-hero.liquid'),'utf8');
hero=hero.replace('<nav class="category-strip shell"','<nav class="category-strip shell"');
hero=hero.replace("{% assign category_handles",'<a class="category-all" href="{{ routes.all_products_collection_url }}">{{ \'general.shop\' | t }}</a>\n{% assign category_handles');
const start=hero.indexOf('<section class="hero shell"'),end=hero.indexOf('{% schema %}');
hero=hero.slice(0,start)+`{% if section.settings.catalog_first %}
<section class="catalog-intro shell" aria-labelledby="FeaturedHeading"><div><p class="eyebrow hero-kicker">{{ section.settings.eyebrow | escape }}</p><h1 id="FeaturedHeading">{{ section.settings.heading | escape }}</h1><p>{{ section.settings.description | escape }}</p></div><a class="button" href="{{ routes.all_products_collection_url }}">{{ section.settings.button_label | escape }} {% render 'studio-icon', name: 'arrow-right' %}</a></section>
{% else %}
`+hero.slice(start,end)+'{% endif %}\n'+hero.slice(end);
hero=hero.replace('"settings":[','"settings":[{"type":"checkbox","id":"catalog_first","label":"Compact introduction with products first","default":false},');
fs.writeFileSync(file('sections/studio-hero.liquid'),hero);
const index=JSON.parse(fs.readFileSync(file('templates/index.json'),'utf8'));
Object.assign(index.sections.hero.settings,{catalog_first:true,eyebrow:'THE ROZMISO COLLECTION',heading:'Home care. Kitchen. Travel.',description:'Explore the products below. Open a product to see its details and care guidance.',button_label:'View all products'});
index.sections.edit.settings.heading='Browse products';
index.sections.edit.block_order=['item0','item2','item3','item1'];
fs.writeFileSync(file('templates/index.json'),JSON.stringify(index,null,2)+'\n');
const videoSnippet=`{% doc %}
Renders only real video media attached to the current Shopify product. No external lookup or placeholder demonstrations.
@param {product} item - Product
{% enddoc %}
{% assign hosted_videos = item.media | where: 'media_type', 'video' %}
{% assign external_videos = item.media | where: 'media_type', 'external_video' %}
{% assign video_count = hosted_videos.size | plus: external_videos.size %}
{% if video_count > 0 %}<section class="product-videos" aria-labelledby="ProductVideoHeading"><h2 id="ProductVideoHeading">{{ 'product.videos' | t }}</h2>
{% for media in item.media %}{% if media.media_type == 'video' or media.media_type == 'external_video' %}<figure class="product-video-frame">
{% if media.media_type == 'video' %}{{ media | video_tag: image_size: '900x', controls: true, autoplay: false, loop: false, preload: 'none', class: 'product-video' }}{% else %}{{ media | external_video_url: autoplay: '0' | external_video_tag: loading: 'lazy', class: 'product-video' }}{% endif %}
{% if media.alt != blank %}<figcaption>{{ media.alt | escape }}</figcaption>{% endif %}</figure>{% endif %}{% endfor %}</section>{% endif %}
`;
fs.writeFileSync(file('snippets/studio-product-videos.liquid'),videoSnippet);
let pdp=fs.readFileSync(file('sections/studio-product.liquid'),'utf8');
const boundary='</div></div>\n<div class="product-info">';
if(!pdp.includes(boundary))throw Error('Product gallery insertion boundary missing');
pdp=pdp.replace(boundary,'</div>{% render \'studio-product-videos\', item: product %}</div>\n<div class="product-info">');
fs.writeFileSync(file('sections/studio-product.liquid'),pdp);
const locale=JSON.parse(fs.readFileSync(file('locales/en.default.json'),'utf8'));locale.product.videos='Product videos';
fs.writeFileSync(file('locales/en.default.json'),JSON.stringify(locale,null,2)+'\n');
let css=fs.readFileSync(file('assets/studio.css'),'utf8');
css=css.replace('/* Responsive rules for the shared system. */',`.catalog-intro{display:flex;align-items:center;justify-content:space-between;gap:32px;padding-block:32px 8px}.catalog-intro h1{font-size:clamp(28px,3.1vw,42px);margin-top:8px}.catalog-intro p:not(.eyebrow){color:var(--muted);font-size:14px;margin-top:12px;max-width:600px}.catalog-intro .button{flex-shrink:0}.category-all{font-weight:700}.product-videos{margin-top:28px}.product-videos h2{font-size:22px;letter-spacing:-.02em;margin-bottom:14px}.product-video-frame{margin:0 0 20px}.product-video{display:block;width:100%;max-height:560px;background:var(--sage);border:0;border-radius:10px}.product-video-frame iframe{aspect-ratio:16/9;max-width:100%}.product-video-frame figcaption{font-size:13px;color:var(--muted);margin-top:8px}
/* Responsive rules for the shared system. */`);
css=css.replace('.category-strip a{min-height:44px;display:flex;align-items:center}', '.category-strip a{min-height:44px;display:flex;align-items:center;white-space:nowrap}.category-strip{font-size:13px}');
css=css.replace(' .hero{display:flex;', ' .catalog-intro{display:block;padding-block:22px 0}.catalog-intro h1{font-size:28px;line-height:1.18}.catalog-intro p:not(.eyebrow){font-size:13px;margin-top:10px}.catalog-intro .button{margin-top:16px;min-height:44px;width:100%}.product-videos h2{font-size:21px}\n .hero{display:flex;');
fs.writeFileSync(file('assets/studio.css'),css);
console.log('Prepared isolated theme: catalog first, mobile Shop all, native product-video support. No supplier media copied or commercial ordering enabled.');
