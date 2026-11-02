from pathlib import Path
p=Path('F:/Dropshipping/rozmiso-studio-theme/layout/theme.liquid')
s=p.read_text(encoding='utf-8-sig')
needle='<script src="{{ \'studio.js\' | asset_url }}" defer></script>'
insert="{% if request.page_type == 'product' %}{{ 'product-bento.css' | asset_url | stylesheet_tag }}<script src=\"{{ 'product-bento.js' | asset_url }}\" defer></script>{% endif %}"
assert needle in s
if "'product-bento.css'" not in s:s=s.replace(needle,needle+insert)
p.write_text(s,encoding='utf-8')
print('Product-only bento assets included.')
