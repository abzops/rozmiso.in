from pathlib import Path
import shutil,json,hashlib
root=Path('F:/Dropshipping'); source=root/'rozmiso-studio-theme'; report=root/'team/reports/T022'; dest=report/'theme-candidate'
if dest.exists():raise SystemExit('Candidate already exists; do not overwrite review work')
shutil.copytree(source,dest)
def change(rel,fn):
 p=dest/rel;t=p.read_text(encoding='utf-8');p.write_text(fn(t),encoding='utf-8')
def replace(t,a,b):
 if a not in t:raise ValueError('Missing expected source: '+a[:100])
 return t.replace(a,b)
change('layout/theme.liquid',lambda t:replace(t,'</head><body>','</head><body data-prelaunch="{{ settings.prelaunch_mode }}">'))
def pdp(t):
 t=replace(t,'{% assign chosen = product.selected_or_first_available_variant %}','{% assign chosen = product.selected_or_first_available_variant %}\n{% assign can_order = chosen.available %}{% if settings.prelaunch_mode %}{% assign can_order = false %}{% endif %}')
 t=t.replace('unless chosen.available','unless can_order').replace('{% if chosen.available %}','{% if can_order %}')
 return t
change('sections/studio-product.liquid',pdp)
for rel in ['sections/studio-header.liquid','templates/cart.liquid']:
 change(rel,lambda t:replace(t,'type="submit" name="checkout">','type="submit" name="checkout" {% if settings.prelaunch_mode %}disabled aria-describedby="PreviewCheckoutNote"{% endif %}>').replace('<p class="small muted">{{ \'cart.checkout_note\' | t }}</p>','<p class="small muted" id="PreviewCheckoutNote">{% if settings.prelaunch_mode %}{{ \'general.launch_notice\' | t }}{% else %}{{ \'cart.checkout_note\' | t }}{% endif %}</p>'))
# Give full cart and drawer notes distinct IDs when rendered on the same page.
change('templates/cart.liquid',lambda t:t.replace('PreviewCheckoutNote','FullCartCheckoutNote'))
change('snippets/studio-card.liquid',lambda t:t.replace('data-available="{{ item.available }}"','data-available="{% if settings.prelaunch_mode %}false{% else %}{{ item.available }}{% endif %}"').replace('{% unless item.available %}','{% if settings.prelaunch_mode or item.available == false %}').replace('{% endunless %}','{% endif %}'))
def js(t):
 t="const rozmisoPrelaunch = document.body.dataset.prelaunch === 'true';\n"+t
 t=replace(t,"button.disabled=option.dataset.available!=='true'","button.disabled=rozmisoPrelaunch||option.dataset.available!=='true'")
 t=replace(t,"const nativeMatches=indexed.map(product=>currentCatalog.find(current=>current.id===String(product.id))).filter(Boolean);", """const nativeMatches=indexed.map(product=>{
            const current=currentCatalog.find(current=>current.id===String(product.id));
            if(current)return current;
            if(!product.id||typeof product.title!=='string'||typeof product.url!=='string')return null;
            let url;try{url=new URL(product.url,location.origin);}catch{return null;}
            if(url.origin!==location.origin||!url.pathname.includes('/products/'))return null;
            // Predictive Search returns decimal currency amounts; Liquid local data is cents.
            const price=Number(product.price);if(!Number.isFinite(price)||price<0)return null;
            return {id:String(product.id),title:product.title,url:url.pathname+url.search,price,available:product.available===true,image:product.featured_image?.url||product.image};
          }).filter(Boolean);""")
 t=t.replace("+(product.available?'':' · '+box.dataset.unavailable)","+(!rozmisoPrelaunch&&product.available?'':' · '+box.dataset.unavailable)")
 marker="  const dialog=document.querySelector('[data-cart-dialog]');"
 t=replace(t,marker,"""  // Prevent theme-managed addition/checkout even without the optional cart drawer.
  document.addEventListener('submit',event=>{
    if(!rozmisoPrelaunch)return;
    const form=event.target;
    if(form.id==='ProductForm'||event.submitter?.name==='checkout')event.preventDefault();
  });
"""+marker)
 t=replace(t,"event.preventDefault();if(button.disabled||busy)return;","event.preventDefault();if(rozmisoPrelaunch||button.disabled||busy)return;")
 t=replace(t,"button.disabled=Boolean(selected&&selected.dataset.available!=='true');","button.disabled=rozmisoPrelaunch||Boolean(selected&&selected.dataset.available!=='true');")
 t=replace(t,"if(selected&&[...product.options].some(option=>option.value===selected))","if(selected&&selected.length<=200)")
 return t
change('assets/studio.js',js)
def contact(t):
 a='<select id="ContactProduct" name="contact[Product]" data-enquiry-product><option value="No specific product">{{ \'general.enquiry_any\' | t }}</option>'
 b='<input id="ContactProduct" name="contact[Product]" data-enquiry-product list="EnquiryProducts" maxlength="200" placeholder="{{ \'general.enquiry_any\' | t }}"><datalist id="EnquiryProducts">'
 t=replace(t,a,b)
 t=replace(t,'</option>{% endfor %}</select><label for="ContactMessage">','</option>{% endfor %}</datalist><label for="ContactMessage">')
 return t
change('templates/page.contact.liquid',contact)
native='''{% if collection.all_products_count > 24 and collection.filters.size > 0 %}
<form action="{{ collection.url }}" method="get" class="catalog-refinements" data-native-filters>
<input type="hidden" name="sort_by" value="{{ current_sort | escape }}">
{% for filter in collection.filters %}
{% unless settings.prelaunch_mode and filter.param_name == 'filter.v.availability' %}
{% case filter.type %}
{% when 'price_range' %}
<div><label for="NativeMinPrice">{{ 'product.price_min' | t }}</label><input id="NativeMinPrice" type="number" min="0" step="0.01" name="{{ filter.min_value.param_name | escape }}" {% if filter.min_value.value %}value="{{ filter.min_value.value | divided_by: 100.0 }}"{% endif %}></div>
<div><label for="NativeMaxPrice">{{ 'product.price_max' | t }}</label><input id="NativeMaxPrice" type="number" min="0" step="0.01" name="{{ filter.max_value.param_name | escape }}" {% if filter.max_value.value %}value="{{ filter.max_value.value | divided_by: 100.0 }}"{% endif %}></div>
{% when 'list', 'boolean' %}
<details><summary>{{ filter.label | escape }}</summary>{% for value in filter.values %}<label class="available-filter"><input type="checkbox" name="{{ value.param_name | escape }}" value="{{ value.value | escape }}" {% if value.active %}checked{% endif %} {% if value.count == 0 and value.active == false %}disabled{% endif %}>{{ value.label | escape }} ({{ value.count }})</label>{% endfor %}</details>
{% endcase %}{% endunless %}{% endfor %}
<button type="submit" class="text-link">{{ 'general.apply' | t }}</button><a class="text-link" href="{{ collection.url }}?sort_by={{ current_sort | url_encode }}">{{ 'product.clear_filters' | t }}</a>
</form>
{% endif %}
'''
def collection(t):
 t=replace(t,'{% if paginate.pages == 1 and collection.products_count > 0 %}','{% if collection.all_products_count <= 24 and collection.products_count > 0 %}')
 t=replace(t,'<div class="product-grid" data-catalog-grid>',native+'<div class="product-grid" data-catalog-grid>')
 # Preserve Shopify filters when sorting; do not discard active catalog-wide filters.
 hidden='''{% for filter in collection.filters %}{% for value in filter.active_values %}<input type="hidden" name="{{ value.param_name | escape }}" value="{{ value.value | escape }}">{% endfor %}{% if filter.type == 'price_range' %}{% if filter.min_value.value %}<input type="hidden" name="{{ filter.min_value.param_name | escape }}" value="{{ filter.min_value.value | divided_by: 100.0 }}">{% endif %}{% if filter.max_value.value %}<input type="hidden" name="{{ filter.max_value.param_name | escape }}" value="{{ filter.max_value.value | divided_by: 100.0 }}">{% endif %}{% endif %}{% endfor %}'''
 t=replace(t,'<form method="get"><label for="SortBy">','<form method="get">'+hidden+'<label for="SortBy">')
 return t
change('sections/studio-collection.liquid',collection)
manifest=[]
for p in source.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(source);new=dest/rel
 before=hashlib.sha256(p.read_bytes()).hexdigest();after=hashlib.sha256(new.read_bytes()).hexdigest()
 if before!=after:manifest.append({'path':rel.as_posix(),'source_sha256':before,'candidate_sha256':after})
(report/'CHANGED-FILES.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
