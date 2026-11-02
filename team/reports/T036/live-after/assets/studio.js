const rozmisoPrelaunch = document.body.dataset.prelaunch === 'true';
// Keep the selected variant, gallery and purchase guidance in sync.
const setProductImage=(root,source,alt,id)=>{
  const image=root.querySelector('#ProductImage');
  if(image&&source){image.src=source;image.alt=alt||'';image.removeAttribute('srcset');}
  root.querySelectorAll('button[data-image]').forEach(button=>button.setAttribute('aria-pressed',String(id?button.dataset.imageId===id:button.dataset.image===source)));
};
document.addEventListener('change',event=>{
  if(!event.target.matches('[data-variants]'))return;
  const select=event.target,root=select.closest('[data-product]'),option=select.selectedOptions[0];if(!root||!option)return;
  root.querySelector('[data-price]').textContent=option.dataset.price;
  const compare=root.querySelector('[data-compare]');compare.textContent=option.dataset.compare;compare.hidden=!option.dataset.compare;
  const unavailable=rozmisoPrelaunch||option.dataset.available!=='true',button=root.querySelector('[data-add]');
  button.disabled=unavailable;button.textContent=unavailable?button.dataset.sold:button.dataset.label;
  root.querySelectorAll('[data-availability-note],[data-product-enquiry]').forEach(element=>element.hidden=!unavailable);
  const quantity=root.querySelector('[name="quantity"]');
  if(quantity){
    const min=Number(option.dataset.min)||1,step=Number(option.dataset.step)||1,max=Number(option.dataset.max);
    quantity.min=String(min);quantity.step=String(step);
    if(option.dataset.max&&Number.isFinite(max))quantity.max=String(max);else quantity.removeAttribute('max');
    let value=Number(quantity.value);if(!Number.isFinite(value)||value<min)value=min;
    value=min+Math.ceil((value-min)/step)*step;
    if(quantity.hasAttribute('max')&&value>max)value=min+Math.floor((max-min)/step)*step;
    quantity.value=String(Math.max(min,value));
  }
  const url=new URL(location.href);url.searchParams.set('variant',option.value);history.replaceState({},'',url);
  if(option.dataset.image)setProductImage(root,option.dataset.image,option.dataset.alt,option.dataset.imageId);
});
document.addEventListener('click',event=>{const button=event.target.closest('button[data-image]');if(!button)return;setProductImage(button.closest('[data-product]'),button.dataset.image,button.dataset.alt,button.dataset.imageId);});
// Commerce features: preserve native search, cart forms and product links as fallbacks.
(() => {
  const root = window.Shopify?.routes?.root || '/';
  const catalogTemplate=document.querySelector('[data-search-catalog]');
  const currentCatalog=catalogTemplate?[...catalogTemplate.content.querySelectorAll('a')].map(link=>({id:link.dataset.id,title:link.dataset.title,url:link.getAttribute('href'),price:Number(link.dataset.price)/100,available:link.dataset.available==='true',image:link.dataset.image,keywords:link.dataset.keywords.toLocaleLowerCase()})):[];
  const searchBoxes = document.querySelectorAll('[data-instant-search]');
  searchBoxes.forEach(box => {
    const input=box.querySelector('[data-search-input]'), results=box.querySelector('[data-search-results]'), status=box.querySelector('[data-search-status]');
    let timer, controller, generation=0;
    const close=()=>{results.hidden=true;input.setAttribute('aria-expanded','false');};
    input.addEventListener('input',()=>{
      clearTimeout(timer);controller?.abort();const current=++generation,q=input.value.trim();
      if(q.length<2){close();results.replaceChildren();status.textContent='';return;}
      timer=setTimeout(async()=>{
        controller=new AbortController();status.textContent=box.dataset.loading;
        try {
          const params=new URLSearchParams({q,'resources[type]':'product','resources[limit]':'5','resources[options][unavailable_products]':'show'});
          const response=await fetch(root+'search/suggest.json?'+params,{signal:controller.signal});
          if(!response.ok)throw new Error('Search failed');
          const data=await response.json();if(current!==generation)return;
          const indexed=data.resources?.results?.products || [];
          const nativeMatches=indexed.map(product=>{
            const current=currentCatalog.find(current=>current.id===String(product.id));
            if(current)return current;
            if(!product.id||typeof product.title!=='string'||typeof product.url!=='string')return null;
            let url;try{url=new URL(product.url,location.origin);}catch{return null;}
            if(url.origin!==location.origin||!url.pathname.includes('/products/'))return null;
            // Predictive Search returns decimal currency amounts; Liquid local data is cents.
            const price=Number(product.price);if(!Number.isFinite(price)||price<0)return null;
            return {id:String(product.id),title:product.title,url:url.pathname+url.search,price,available:product.available===true,image:product.featured_image?.url||product.image};
          }).filter(Boolean);
          const words=q.toLocaleLowerCase().split(/\s+/).filter(Boolean);
          const fallbackMatches=currentCatalog.filter(product=>words.every(word=>product.keywords.includes(word)));
          const products=[...new Map([...nativeMatches,...fallbackMatches].map(product=>[product.id,product])).values()].slice(0,5);results.replaceChildren();
          products.forEach(product=>{
            const url=new URL(product.url,location.origin);if(url.origin!==location.origin)return;
            const link=document.createElement('a');link.href=url.pathname+url.search;link.className='search-match';
            const source=product.featured_image?.url || product.image;
            if(source){const image=document.createElement('img');image.src=source;image.alt='';image.width=54;image.height=54;link.append(image);}
            const text=document.createElement('span'),title=document.createElement('strong'),meta=document.createElement('small');title.textContent=product.title;
            meta.textContent=new Intl.NumberFormat(document.documentElement.lang||'en-IN',{style:'currency',currency:box.dataset.currency||'INR'}).format(Number(product.price))+(!rozmisoPrelaunch&&product.available?'':' · '+box.dataset.unavailable);
            text.append(title,meta);link.append(text);results.append(link);
          });
          if(!products.length){const empty=document.createElement('p');empty.textContent=box.dataset.noResults;results.append(empty);}
          const all=document.createElement('a');all.className='search-view-all';all.href=root+'search?type=product&q='+encodeURIComponent(q);all.textContent=window.rozmisoLabels.searchAll;results.append(all);
          results.hidden=false;input.setAttribute('aria-expanded','true');status.textContent=products.length+' '+window.rozmisoLabels.searchMatches;
        } catch(error){if(error.name==='AbortError'||current!==generation)return;close();status.textContent=window.rozmisoLabels.searchFailure;}
      },200);
    });
    input.addEventListener('keydown',event=>{if(event.key==='Escape'){close();controller?.abort();generation++;}if(event.key==='ArrowDown'&&!results.hidden){event.preventDefault();results.querySelector('a')?.focus();}});
    results.addEventListener('keydown',event=>{const links=[...results.querySelectorAll('a')],index=links.indexOf(document.activeElement);if(event.key==='Escape'){close();input.focus();}if(event.key==='ArrowDown'){event.preventDefault();links[(index+1)%links.length]?.focus();}if(event.key==='ArrowUp'){event.preventDefault();if(index<=0)input.focus();else links[index-1]?.focus();}});
    document.addEventListener('click',event=>{if(!box.contains(event.target))close();});
  });

  document.querySelectorAll('[data-catalog]').forEach(catalog=>{
    const chips=[...catalog.querySelectorAll('[data-filter]')],cards=[...catalog.querySelectorAll('[data-catalog-grid] .product-card')];
    const min=catalog.querySelector('[data-price-min]'),max=catalog.querySelector('[data-price-max]'),available=catalog.querySelector('[data-only-available]');
    catalog.querySelectorAll('[data-category-filters],[data-catalog-refinements]').forEach(el=>el.hidden=false);
    const params=new URLSearchParams(location.search),category=params.get('category')||'all';
    if(chips.some(chip=>chip.dataset.filter===category))chips.forEach(chip=>chip.setAttribute('aria-pressed',String(chip.dataset.filter===category)));
    if(min)min.value=params.get('min_price')||'';if(max)max.value=params.get('max_price')||'';if(available)available.checked=params.get('available')==='true';
    const apply=(updateUrl=true)=>{
      const selected=chips.find(chip=>chip.getAttribute('aria-pressed')==='true')?.dataset.filter||'all';
      const low=min?.value.trim()?Number(min.value)*100:0,high=max?.value.trim()?Number(max.value)*100:Infinity;
      let count=0;cards.forEach(card=>{const price=Number(card.dataset.productPrice),show=(selected==='all'||card.dataset.category===selected)&&price>=low&&price<=high&&(!available?.checked||card.dataset.available==='true');card.hidden=!show;if(show)count++;});
      if(chips.length||min){catalog.querySelector('[data-result-count]').textContent=count+' '+(count===1?window.rozmisoLabels.product:window.rozmisoLabels.products);const empty=catalog.querySelector('[data-filter-empty]');if(empty)empty.hidden=count!==0;}
      const url=new URL(location.href);[['category',selected==='all'?'':selected],['min_price',min?.value||''],['max_price',max?.value||''],['available',available?.checked?'true':'']].forEach(([key,value])=>{if(value)url.searchParams.set(key,value);else url.searchParams.delete(key);});
      if(updateUrl)history.replaceState({},'',url);
      const form=catalog.querySelector('[data-auto-sort]')?.form;if(form){form.querySelectorAll('[data-preserved-filter]').forEach(el=>el.remove());['category','min_price','max_price','available'].forEach(name=>{const value=url.searchParams.get(name);if(value){const hidden=document.createElement('input');hidden.type='hidden';hidden.name=name;hidden.value=value;hidden.dataset.preservedFilter='';form.append(hidden);}});}
    };
    chips.forEach(chip=>chip.addEventListener('click',()=>{chips.forEach(c=>c.setAttribute('aria-pressed',String(c===chip)));apply();}));
    [min,max,available].filter(Boolean).forEach(input=>input.addEventListener('input',()=>apply()));
    catalog.querySelector('[data-filter-reset]')?.addEventListener('click',()=>{chips.forEach(chip=>chip.setAttribute('aria-pressed',String(chip.dataset.filter==='all')));if(min)min.value='';if(max)max.value='';if(available)available.checked=false;apply();});
    if(chips.length||min)apply(false);
  });
  document.addEventListener('change',event=>{if(event.target.matches('[data-auto-sort]'))event.target.form.requestSubmit();});

  const imageDialog=document.querySelector('[data-image-dialog]');
  const zoom=trigger=>{const source=trigger.querySelector('img');if(!source||!imageDialog?.showModal)return;const target=imageDialog.querySelector('[data-zoom-target]');target.src=source.currentSrc||source.src;target.alt=source.alt;imageDialog.showModal();};
  document.addEventListener('click',event=>{const trigger=event.target.closest('[data-zoom-image]');if(trigger)zoom(trigger);if(event.target.closest('[data-close-image]'))imageDialog?.close();});
  document.addEventListener('keydown',event=>{if(event.target.matches('[data-zoom-image]')&&['Enter',' '].includes(event.key)){event.preventDefault();zoom(event.target);}});
  imageDialog?.addEventListener('click',event=>{if(event.target===imageDialog)imageDialog.close();});

  // Prevent theme-managed addition/checkout even without the optional cart drawer.
  document.addEventListener('submit',event=>{
    if(!rozmisoPrelaunch)return;
    const form=event.target;
    if(form.id==='ProductForm'||event.submitter?.name==='checkout')event.preventDefault();
  });
  const dialog=document.querySelector('[data-cart-dialog]');
  if(!dialog?.showModal)return;
  let busy=false,returnFocus;
  const errorBox=dialog.querySelector('[data-cart-error]');
  const showError=message=>{errorBox.textContent=message;errorBox.hidden=false;};
  const setBusy=value=>{busy=value;dialog.setAttribute('aria-busy',String(value));dialog.querySelectorAll('[data-cart-quantity]').forEach(input=>input.disabled=value);};
  const refresh=async()=>{
    const response=await fetch(root+'?section_id=studio-header');if(!response.ok)throw new Error('Cart could not be loaded');
    const html=new DOMParser().parseFromString(await response.text(),'text/html'),content=html.querySelector('[data-cart-content]');
    if(!content)throw new Error('Cart content missing');dialog.querySelector('[data-cart-content]').replaceWith(content);
    document.querySelectorAll('[data-cart-badge]').forEach(badge=>badge.textContent=content.dataset.count);
  };
  const open=async trigger=>{returnFocus=trigger;errorBox.hidden=true;dialog.showModal();setBusy(true);try{await refresh();}catch{showError(window.rozmisoLabels.cartError);}finally{setBusy(false);}};
  const change=async(key,quantity)=>{
    if(busy)return;setBusy(true);errorBox.hidden=true;
    try {const response=await fetch(root+'cart/change.js',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({id:key,quantity})});const data=await response.json();if(!response.ok)throw new Error(data.description||data.message||window.rozmisoLabels.cartError);await refresh();}
    catch(error){try{await refresh();}catch{}showError(error.name==='TypeError'?window.rozmisoLabels.cartError:(error.message||window.rozmisoLabels.cartError));}finally{setBusy(false);}
  };
  document.addEventListener('click',event=>{
    const trigger=event.target.closest('[data-open-cart]');if(trigger){event.preventDefault();if(!dialog.open)open(trigger);}
    if(event.target.closest('[data-close-cart]'))dialog.close();
    const remove=event.target.closest('[data-cart-remove]');if(remove){event.preventDefault();change(remove.dataset.key,0);}
  });
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});dialog.addEventListener('close',()=>returnFocus?.focus());
  dialog.addEventListener('change',event=>{const input=event.target;if(input.matches('[data-cart-quantity]')){if(input.checkValidity())change(input.dataset.key,Number(input.value));else input.reportValidity();}});
  document.addEventListener('submit',async event=>{
    const form=event.target;if(form.id!=='ProductForm')return;const button=form.querySelector('[data-add]');if(!button)return;
    event.preventDefault();if(rozmisoPrelaunch||button.disabled||busy)return;setBusy(true);button.disabled=true;const label=button.textContent;button.textContent=window.rozmisoLabels.adding;
    try {const response=await fetch(root+'cart/add.js',{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});const data=await response.json();if(!response.ok)throw new Error(data.description||data.message||window.rozmisoLabels.cartError);returnFocus=button;if(!dialog.open)dialog.showModal();errorBox.hidden=true;await refresh();}
    catch(error){if(!dialog.open){returnFocus=button;dialog.showModal();}showError(error.message||window.rozmisoLabels.cartError);}
    finally{setBusy(false);const selected=form.querySelector('[data-variants] option:checked');button.disabled=rozmisoPrelaunch||Boolean(selected&&selected.dataset.available!=='true');button.textContent=button.disabled?button.dataset.sold:label;}
  });
})();

// Mobile navigation keeps native details behavior and supports dismissal.
(()=>{const menu=document.querySelector('.mobile-menu');if(!menu)return;document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.open){menu.open=false;menu.querySelector('summary').focus();}});document.addEventListener('click',event=>{if(menu.open&&!menu.contains(event.target))menu.open=false;});})();

// Prefill only a current product option from the product enquiry link.
(()=>{const product=document.querySelector('[data-enquiry-product]');if(!product)return;const selected=new URLSearchParams(location.search).get('product');if(!product.value&&selected&&selected.length<=200){product.value=selected;const topic=document.querySelector('[data-enquiry-topic]');if(topic)topic.value='Product availability';}})();

// Touch gallery: reuse thumbnail selection; preserve page scrolling, pinch and tap-to-zoom.
(() => {
  document.querySelectorAll('[data-product]').forEach(root => {
    const frame = root.querySelector('[data-zoom-image]');
    const slides = [...root.querySelectorAll('button[data-image]')];
    if (!frame || slides.length < 2) return;
    frame.style.touchAction = 'pan-y pinch-zoom';
    let gesture = null;
    let suppressClickUntil = 0;
    const pointers = new Set();
    frame.addEventListener('pointerdown', event => {
      if (!['touch', 'pen'].includes(event.pointerType)) return;
      pointers.add(event.pointerId);
      if (pointers.size !== 1 || event.isPrimary === false) {
        gesture = null;
        suppressClickUntil = Date.now() + 700;
        return;
      }
      suppressClickUntil = 0;
      gesture = {id:event.pointerId, x:event.clientX, y:event.clientY, moved:false};
      if (frame.setPointerCapture) frame.setPointerCapture(event.pointerId);
    });
    frame.addEventListener('pointermove', event => {
      if (!gesture || gesture.id !== event.pointerId) return;
      if (Math.hypot(event.clientX - gesture.x, event.clientY - gesture.y) > 12) gesture.moved = true;
    });
    frame.addEventListener('pointerup', event => {
      pointers.delete(event.pointerId);
      if (!gesture || gesture.id !== event.pointerId) return;
      const {x, y, moved} = gesture;
      gesture = null;
      const dx = event.clientX - x;
      const dy = event.clientY - y;
      if (moved || Math.hypot(dx, dy) > 12) suppressClickUntil = Date.now() + 700;
      const threshold = Math.min(72, Math.max(36, frame.clientWidth * .08));
      if (Math.abs(dx) < threshold || Math.abs(dx) <= Math.abs(dy) * 1.25) return;
      const selected = slides.findIndex(button => button.getAttribute('aria-pressed') === 'true');
      const index = Math.max(0, selected);
      slides[(index + (dx < 0 ? 1 : -1) + slides.length) % slides.length].click();
    });
    const cancel = event => {
      pointers.delete(event.pointerId);
      if (gesture?.id === event.pointerId) {
        gesture = null;
        suppressClickUntil = Date.now() + 700;
      }
    };
    frame.addEventListener('pointercancel', cancel);
    frame.addEventListener('lostpointercapture', cancel);
    frame.addEventListener('click', event => {
      if (Date.now() >= suppressClickUntil || event.detail === 0) return;
      event.preventDefault();
      event.stopPropagation();
    }, true);
  });
})();

