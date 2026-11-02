import json
from pathlib import Path

root = Path('F:/Dropshipping/rozmiso-studio-theme')
path = root / 'locales/en.default.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['cart']['unavailable_note'] = 'Checkout is currently unavailable. Contact us for help with the items in your bag.'
data['product']['shaver_a3'] = 'Use the charging connection shown with the product and follow the included instructions for the required power supply and charging guidance.'
data['general']['personal_care'] = 'Personal care'
data['general']['other_essentials'] = 'Other essentials'
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
path = root / 'templates/cart.liquid'
path.write_text(path.read_text(encoding='utf-8').replace("'general.launch_notice'", "'cart.unavailable_note'"), encoding='utf-8')
path = root / 'sections/studio-header.liquid'
source = path.read_text(encoding='utf-8')
marker = source.index('<dialog class=')
source = source[:marker] + source[marker:].replace("'general.launch_notice'", "'cart.unavailable_note'")
path.write_text(source, encoding='utf-8')
path = root / 'assets/studio.css'
source = path.read_text(encoding='utf-8').replace(
    '.rte h2{font-family:inherit;letter-spacing:0;font-size:20px;margin-top:25px}',
    ".rte h2,.rte h3{font-family:Georgia,'Times New Roman',serif;letter-spacing:-.015em;color:var(--ink);font-size:23px;line-height:1.3;margin-top:25px}.thumbs button[aria-pressed=true]{border:2px solid var(--ink)}"
)
path.write_text(source, encoding='utf-8')
