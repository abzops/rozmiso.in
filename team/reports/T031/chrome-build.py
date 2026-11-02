from pathlib import Path

root=Path('F:/Dropshipping/rozmiso-studio-theme')
header=root/'sections/studio-header.liquid'
old=header.read_text(encoding='utf-8-sig')
dialog=old[old.index('<dialog class="cart-drawer"'):]
header.write_text('''<header class="header reference-header">
  <div class="shell header-row">
    <a class="wordmark" href="{{ routes.root_url }}" aria-label="{{ shop.name | escape }}">{% render 'studio-logo' %}</a>
    <nav class="desktop-nav" aria-label="{{ 'general.navigation' | t }}">
      <a href="{{ routes.all_products_collection_url }}">{{ 'general.shop' | t }}</a>
      {% if collections['home-care'] != blank %}<a href="{{ collections['home-care'].url }}">{{ 'general.home_care' | t }}</a>{% endif %}
      {% if collections['kitchen-essentials'] != blank %}<a href="{{ collections['kitchen-essentials'].url }}">{{ 'general.kitchen' | t }}</a>{% endif %}
      {% if collections['travel-essentials'] != blank %}<a href="{{ collections['travel-essentials'].url }}">{{ 'general.travel' | t }}</a>{% endif %}
      <a href="{{ routes.all_products_collection_url }}?category=personal-care">{{ 'general.personal_care' | t }}</a>
    </nav>
    <div class="header-search-row">
      <div class="instant-search" data-instant-search data-no-results="{{ 'product.no_results' | t }}" data-loading="{{ 'general.search_loading' | t }}" data-unavailable="{{ 'product.sold_out' | t }}" data-currency="{{ shop.currency }}">
        <form action="{{ routes.search_url }}" method="get" role="search">
          <label class="sr-only" for="HeaderSearch">{{ 'general.search' | t }}</label>
          <input id="HeaderSearch" type="search" name="q" placeholder="Search the collection..." autocomplete="off" aria-expanded="false" aria-controls="HeaderSuggestions" data-search-input>
          <input type="hidden" name="type" value="product">
          <button type="submit" aria-label="{{ 'general.search' | t }}">{% render 'studio-icon', name: 'search' %}</button>
        </form>
        <div id="HeaderSuggestions" class="search-suggestions" hidden data-search-results></div>
        <span class="sr-only" role="status" data-search-status></span>
      </div>
    </div>
    <div class="header-actions">
      <a class="bag-link" aria-label="{{ 'cart.bag' | t }}" href="{{ routes.cart_url }}" data-open-cart>{% render 'studio-icon', name: 'bag' %}<span class="bag-label">{{ 'cart.bag' | t }}</span><span data-cart-badge>{{ cart.item_count }}</span></a>
      <details class="mobile-menu">
        <summary aria-label="{{ 'general.navigation' | t }}">{% render 'studio-icon', name: 'menu' %}</summary>
        <nav aria-label="{{ 'general.navigation' | t }}">
          <a href="{{ routes.all_products_collection_url }}">{{ 'general.shop' | t }}</a>
          {% if collections['home-care'] != blank %}<a href="{{ collections['home-care'].url }}">{{ 'general.home_care' | t }}</a>{% endif %}
          {% if collections['kitchen-essentials'] != blank %}<a href="{{ collections['kitchen-essentials'].url }}">{{ 'general.kitchen' | t }}</a>{% endif %}
          {% if collections['travel-essentials'] != blank %}<a href="{{ collections['travel-essentials'].url }}">{{ 'general.travel' | t }}</a>{% endif %}
          <a href="{{ routes.all_products_collection_url }}?category=personal-care">{{ 'general.personal_care' | t }}</a>
          <a href="{{ routes.root_url }}pages/contact">{{ 'general.help' | t }}</a>
          <a href="{{ routes.root_url }}#our-approach">{{ 'general.about' | t }}</a>
        </nav>
      </details>
    </div>
  </div>
</header>
''' + dialog,encoding='utf-8')

footer='''<footer class="footer reference-footer">
  <div class="shell">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="wordmark" href="{{ routes.root_url }}" aria-label="{{ shop.name | escape }}">{% render 'studio-logo', reversed: true %}</a>
        <p>Practical finds for home care, kitchen<br>routines and travel.</p>
      </div>
      <div>
        <h2 class="footer-heading">Shop</h2>
        <a href="{{ routes.all_products_collection_url }}">{{ 'general.shop' | t }}</a>
        {% if collections['home-care'] != blank %}<a href="{{ collections['home-care'].url }}">{{ 'general.home_care' | t }}</a>{% endif %}
        {% if collections['kitchen-essentials'] != blank %}<a href="{{ collections['kitchen-essentials'].url }}">{{ 'general.kitchen' | t }}</a>{% endif %}
        {% if collections['travel-essentials'] != blank %}<a href="{{ collections['travel-essentials'].url }}">{{ 'general.travel' | t }}</a>{% endif %}
        <a href="{{ routes.all_products_collection_url }}?category=personal-care">{{ 'general.personal_care' | t }}</a>
        <a href="{{ routes.all_products_collection_url }}?category=other-essentials">{{ 'general.other_essentials' | t }}</a>
      </div>
      <div>
        <h2 class="footer-heading">Help &amp; support</h2>
        <a href="{{ routes.root_url }}pages/contact">Get in touch</a>
        {% for policy in shop.policies %}{% if policy.body != blank %}<a href="{{ policy.url }}">{{ policy.title | escape }}</a>{% endif %}{% endfor %}
      </div>
      <div class="footer-social">
        <h2 class="footer-heading">Follow us</h2>
        <div class="footer-social-links">
          <a href="https://www.instagram.com/rozmiso.in/" aria-label="Rozmiso on Instagram" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://www.facebook.com/profile.php?id=61595107991994" aria-label="Rozmiso on Facebook" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="currentColor" stroke="none"/><path d="M13.5 21v-8h2.6l.4-3h-3V8.2c0-.9.3-1.5 1.6-1.5h1.6V4.1A19 19 0 0 0 14.4 4C12.1 4 10.5 5.4 10.5 8v2H8v3h2.5v8" stroke="#103e32" stroke-width="1.2" fill="#103e32"/></svg></a>
        </div>
      </div>
    </div>
    <div class="footer-bottom"><span>© {{ 'now' | date: '%Y' }} {{ shop.name | escape }}</span><span>Home care. Kitchen. Travel.</span></div>
  </div>
</footer>
{% schema %}
{"name":"Studio footer","settings":[]}
{% endschema %}
'''
(root/'sections/studio-footer.liquid').write_text(footer,encoding='utf-8')

layout=root/'layout/theme.liquid';text=layout.read_text(encoding='utf-8-sig')
text=text.replace("{{ 'studio.css' | asset_url | stylesheet_tag }}", "{{ 'studio.css' | asset_url | stylesheet_tag }}{{ 'landing-chrome.css' | asset_url | stylesheet_tag }}{% if request.page_type == 'index' %}{{ 'landing.css' | asset_url | stylesheet_tag }}<script src=\"{{ 'landing.js' | asset_url }}\" defer></script>{% endif %}")
text=text.replace('<body data-prelaunch=', '<body class="{% if request.page_type == \'index\' %}reference-landing{% endif %}" data-prelaunch=')
layout.write_text(text,encoding='utf-8')
