from pathlib import Path
import sys, json, html, base64, shutil
from functools import lru_cache
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools'))
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
OUT=ROOT/'review-kit'
(OUT/'logos').mkdir(parents=True,exist_ok=True)
(OUT/'icons').mkdir(exist_ok=True)
(OUT/'photos').mkdir(exist_ok=True)
font=instantiateVariableFont(TTFont(ROOT/'fonts'/'Manrope-Variable.ttf'),{'wght':750},inplace=False)
glyphs=font.getGlyphSet(); cmap=font.getBestCmap(); units=font['head'].unitsPerEm
FOREST='#26342e'; CREAM='#fbfaf6'; MUTED='#65706a'; CLAY='#b75132'; SAGE='#e8ece1'
def word(text,x,y,size,color=FOREST,tracking=-.027):
    pen=SVGPathPen(glyphs); scale=size/units; cursor=x
    for ch in text:
        glyph=glyphs[cmap[ord(ch)]]
        glyph.draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)))
        cursor+=glyph.width*scale+size*tracking
    return f'<path fill="{color}" d="{pen.getCommands()}"/>',cursor-x
def svg(w,h,body,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>{body}</svg>'
def mark(x,y,size,bg=FOREST,fg=CREAM):
    tile=f'<rect width="32" height="32" rx="8" fill="{bg}"/>' if bg!='none' else ''
    return f'<g transform="translate({x} {y}) scale({size/32})">{tile}<path fill="{fg}" fill-rule="evenodd" d="M9 7h8a7 7 0 0 1 0 14h-3v5H9V7Zm5 5v4h3a2 2 0 0 0 0-4h-3Z"/><path fill="{fg}" d="m17 18 8 8h-7l-6-7Z"/></g>'
logos={}
def logo(name,kind,color=FOREST,bg=FOREST,fg=CREAM):
    if kind=='primary':
        text,width=word('Rozmiso',114,88,80,color)
        value=svg(round(114+width+20),120,mark(20,20,80,bg,fg)+text,'Rozmiso primary logo')
    elif kind=='wordmark':
        text,width=word('Rozmiso',12,78,80,color)
        value=svg(round(width+24),100,text,'Rozmiso wordmark')
    elif kind=='stacked':
        text,width=word('Rozmiso',0,218,64,color)
        text,_=word('Rozmiso',(320-width)/2,218,64,color)
        value=svg(320,246,mark(100,20,120,bg,fg)+text,'Rozmiso stacked logo')
    else:
        value=svg(32,32,mark(0,0,32,bg,fg),'Rozmiso monogram')
    logos[name]=value
    (OUT/'logos'/f'{name}.svg').write_text(value,encoding='utf-8')
logo('rozmiso-primary','primary')
logo('rozmiso-primary-reversed','primary',CREAM,CREAM,FOREST)
logo('rozmiso-primary-black','primary','#000','#000','#fff')
logo('rozmiso-primary-white','primary','#fff','#fff','#000')
logo('rozmiso-wordmark','wordmark')
logo('rozmiso-wordmark-reversed','wordmark',CREAM)
logo('rozmiso-stacked','stacked')
logo('rozmiso-stacked-reversed','stacked',CREAM,CREAM,FOREST)
logo('rozmiso-mark','mark')
logo('rozmiso-mark-reversed','mark',CREAM,CREAM,FOREST)
logo('rozmiso-mark-black','mark','#000','#000','#fff')
icons={
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'bag':'<path d="M5 7h14l1 14H4L5 7Z"/><path d="M8 8V6a4 4 0 0 1 8 0v2"/>',
 'menu':'<path d="M4 6h16M4 12h16M4 18h16"/>',
 'close':'<path d="m6 6 12 12M18 6 6 18"/>',
 'arrow-right':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'chevron-down':'<path d="m6 9 6 6 6-6"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'minus':'<path d="M5 12h14"/>',
 'home':'<path d="m3 10 9-7 9 7v11H3V10Z"/><path d="M9 21v-8h6v8"/>',
 'support':'<path d="M5 12V9a7 7 0 0 1 14 0v3"/><rect x="3" y="10" width="4" height="8" rx="2"/><rect x="17" y="10" width="4" height="8" rx="2"/><path d="M19 18v2h-7"/>',
 'filter':'<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2" fill="currentColor"/><circle cx="16" cy="12" r="2" fill="currentColor"/><circle cx="10" cy="18" r="2" fill="currentColor"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 6 8 7 8-7"/>'
}
def icon(name,x=0,y=0,size=24,color=FOREST):
    return f'<g transform="translate({x} {y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{icons[name]}</g>'
symbols=[]
for name,body in icons.items():
    value=svg(24,24,f'<g fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}</g>',name+' icon')
    (OUT/'icons'/f'{name}.svg').write_text(value,encoding='utf-8')
    symbols.append(f'<symbol id="icon-{name}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{body}</g></symbol>')
(OUT/'icons'/'rozmiso-icons.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(symbols)+'</svg>',encoding='utf-8')
@lru_cache(maxsize=12)
def typeface(family,weight):
    filename='Manrope-Variable.ttf' if family=='Manrope' else 'DMSans-Variable.ttf'
    vf=TTFont(ROOT/'fonts'/filename)
    axes={'wght':weight}
    if family=='DM Sans': axes['opsz']=14
    instance=instantiateVariableFont(vf,axes,inplace=False)
    return instance.getGlyphSet(),instance.getBestCmap(),instance['head'].unitsPerEm
def text(x,y,value,size=16,color=FOREST,weight=400):
    family='Manrope' if size>=22 else 'DM Sans'
    local_glyphs,local_cmap,local_units=typeface(family,weight)
    pen=SVGPathPen(local_glyphs);scale=size/local_units;cursor=x
    for ch in value:
        glyph=local_glyphs[local_cmap[ord(ch)]]
        glyph.draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)))
        cursor+=glyph.width*scale
    return f'<path aria-label="{html.escape(value)}" data-font="{family}" fill="{color}" d="{pen.getCommands()}"/>'
def nested(value,x,y,w,h):
    # Fixed outer sizing preserves each logo's viewBox and aspect ratio.
    value=value.replace('<svg ',f'<svg x="{x}" y="{y}" ',1)
    import re
    return re.sub(r'width="[^"]+" height="[^"]+"',f'width="{w}" height="{h}"',value,count=1)
board=[f'<rect width="1000" height="1080" fill="{CREAM}"/>',text(48,50,'ROZMISO / IDENTITY DIRECTION',12,MUTED,700),text(48,99,'A complete identity. One consistent brand.',32,FOREST,700),text(48,128,'Review draft - existing R mark retained; vector wordmarks and icons added.',16,MUTED)]
board.extend([f'<rect x="48" y="165" width="904" height="180" rx="12" fill="white"/>',nested(logos['rozmiso-primary'],90,195,500,120),text(90,326,'01 / PRIMARY HORIZONTAL',11,MUTED,700)])
board.extend([f'<rect x="48" y="365" width="440" height="164" rx="12" fill="{FOREST}"/>',nested(logos['rozmiso-primary-reversed'],72,388,390,104),text(72,510,'02 / REVERSED',11,CREAM,700)])
board.extend([f'<rect x="512" y="365" width="440" height="164" rx="12" fill="white"/>',nested(logos['rozmiso-wordmark'],540,390,370,100),text(540,510,'03 / WORDMARK ONLY',11,MUTED,700)])
board.extend([text(48,570,'COMPACT MARK / FAVICONS',12,MUTED,700),mark(48,590,88),mark(160,620,32),mark(220,628,16),text(154,674,'32 px',12,MUTED),text(212,674,'16 px',12,MUTED),nested(logos['rozmiso-primary-black'],310,578,290,90),text(320,674,'ONE COLOR',12,MUTED)])
board.append(text(48,724,'PALETTE',12,MUTED,700))
for i,(name,color) in enumerate([('Forest',FOREST),('Cream',CREAM),('Sage',SAGE),('Clay',CLAY)]):
    x=48+i*226; board.append(f'<rect x="{x}" y="744" width="202" height="74" rx="8" fill="{color}" stroke="#dfe2d9"/>');board.append(text(x,842,name+' '+color,14,MUTED))
board.append(text(48,892,'FUNCTIONAL ICONS / 24 px / 1.75 stroke',12,MUTED,700))
for i,name in enumerate(icons):
    x=58+i*74;board.append(icon(name,x,913,28))
board.extend([text(48,987,'Manrope identity and headings / DM Sans body and controls',17,FOREST,700),text(48,1018,'Use specific product facts. No fake reviews, shipping promises or urgency.',15,MUTED),text(48,1045,'Small header: monogram + wordmark. No microscopic descriptor.',15,MUTED)])
(OUT/'IDENTITY-BOARD.svg').write_text(svg(1000,1080,''.join(board),'Rozmiso identity review board'),encoding='utf-8')
asset_root=Path('C:/Users/Abhinand/AppData/Local/Temp/browser-use/assets/6ac6aa00-85b8-4fbb-8f0c-e1e139001835')
sources=[('fabric-shaver','1c67e9ac8ff9b44b.jpg'),('cleaning-brush','ef6219792385195e.jpg'),('soap-brush','2ca622536a2ad13a.jpg'),('travel-organizer','87981609008a34fb.jpg')]
photos={}
for name,filename in sources:
    shutil.copyfile(asset_root/filename,OUT/'photos'/f'{name}.jpg')
    photos[name]='data:image/jpeg;base64,'+base64.b64encode((asset_root/filename).read_bytes()).decode()
def photo(name,x,y,w,h):
    return f'<image href="{photos[name]}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'
phone=[f'<rect width="390" height="1430" fill="{CREAM}"/>',f'<rect width="390" height="28" fill="{FOREST}"/>',text(42,18,'Collection preview - orders are not open yet',11,CREAM),nested(logos['rozmiso-primary'],16,40,157,38),icon('bag',292,46,22),icon('menu',341,46,22),f'<rect x="16" y="96" width="358" height="44" rx="8" fill="white" stroke="#dfe2d9"/>',icon('search',30,108,20),text(61,124,'Search everyday essentials',15,MUTED)]
for label,x,w in [('Home care',16,108),('Kitchen',134,108),('Travel',252,122)]:
    phone.extend([f'<rect x="{x}" y="156" width="{w}" height="38" rx="7" fill="{SAGE if x==16 else CREAM}" stroke="#dfe2d9"/>',text(x+15,180,label,14,FOREST,600)])
phone.extend([text(16,228,'HOME CARE / FEATURED FIND',10,MUTED,700),text(16,267,'A fresh start for',32,FOREST,700),text(16,302,'your favourite fabrics.',32,FOREST,700),photo('fabric-shaver',16,322,358,230),text(16,578,'USB Rechargeable Fabric Shaver',17,FOREST,700),text(16,604,'Rs. 799.00',17,FOREST,700),text(132,604,'Not available yet',13,MUTED),f'<rect x="16" y="626" width="358" height="46" rx="8" fill="{FOREST}"/>',text(31,655,'Explore the collection',15,CREAM,700),icon('arrow-right',335,637,24,CREAM),text(16,719,'Find your everyday helper',23,FOREST,700),text(16,744,'Clear details. Current prices. Actual availability.',13,MUTED)])
for i,(name,title,subtitle,price) in enumerate([('cleaning-brush','Rechargeable','cleaning brush','649'),('travel-organizer','Everyday travel','organizer pouch','349'),('soap-brush','Soap dispensing','cleaning brush','299'),('fabric-shaver','Rechargeable','fabric shaver','799')]):
    x=16+(i%2)*185;y=764+(i//2)*260
    phone.extend([f'<rect x="{x}" y="{y}" width="173" height="244" rx="8" fill="white" stroke="#dfe2d9"/>',photo(name,x+8,y+8,157,132),text(x+10,y+163,title,14,FOREST,600),text(x+10,y+183,subtitle,14,FOREST,600),text(x+10,y+209,'Rs. '+price+'.00',15,FOREST,700),text(x+10,y+230,'Not available yet',12,MUTED)])
phone.extend([f'<rect x="16" y="1298" width="358" height="90" rx="8" fill="{SAGE}"/>',text(32,1327,'A question about a product?',17,FOREST,700),text(32,1351,'Use the contact form before you choose.',13,MUTED),text(32,1374,'Get in touch',14,FOREST,700),text(16,1418,'Rozmiso / Concept only - not a deployed page',11,MUTED)])
(OUT/'MOBILE-CONCEPT.svg').write_text(svg(390,1430,''.join(phone),'Rozmiso mobile homepage concept'),encoding='utf-8')
og=[f'<rect width="1200" height="630" fill="{FOREST}"/>',nested(logos['rozmiso-primary-reversed'],84,132,725,170),text(84,372,'Everyday essentials for home, kitchen and travel.',30,CREAM),text(84,527,'ROZMISO',16,'#c3ccc5',700)]
(OUT/'SHARE-CARD.svg').write_text(svg(1200,630,''.join(og),'Rozmiso social share card'),encoding='utf-8')
shutil.copyfile(ROOT/'fonts'/'OFL.txt',OUT/'FONT-LICENSE.txt')
shutil.copyfile(ROOT/'fonts'/'DM-Sans-OFL.txt',OUT/'DM-SANS-FONT-LICENSE.txt')
(OUT/'README.md').write_text('''# Rozmiso identity and mobile direction - review draft

Prepared 6 October 2026. This kit extends the existing R identity; it does not rename the store or certify trademark availability. No storefront change is deployed.

Start with IDENTITY-BOARD.png and MOBILE-CONCEPT.png. The concept reuses the four exact existing storefront photos. They are supplier media, not new photographs or AI-generated product demonstrations; supplier permission and sample verification remain separate requirements.

## Identity files

Eleven SVG logo variants: horizontal primary, reversed, black/white, wordmark-only, stacked and compact marks. Wordmarks are Manrope 750 converted to vector outlines, so they do not depend on a font being installed. Logo vectors remain editable paths. Transparent PNG exports accompany the primary variants. The existing R paths are preserved.

Use at least 150px width for the complete horizontal logo and 120px for the wordmark-only version; inspect actual output at the intended size. Use the R at compact 16/32px favicon sizes. Clear space is at least a quarter of the mark's height. Do not stretch, add gradients, shadows, outlines or a tiny header subtitle. The reversed lockup has a cream tile and forest R, plus cream wordmark, and belongs on dark surfaces.

The 12 functional icons use a 24px grid, 1.75px strokes and round ends. They are interface symbols, not trust/payment certifications. Maintain a comfortable 44px control hit area when implementing them; icons themselves are not hit areas. Labels or accessible names must accompany controls.

## Mobile concept

390px design board with a compact header, readable search, category navigation, a clearly identified actual product and one primary collection action. Product cards begin earlier than in the current layout. This is a composition concept, not a working Shopify theme or a claim of tested conversion improvement. All products remain marked unavailable. No checkout, sales or shipping promises are invented.

Before live implementation, review at 320/360/390/430px, check long names and text scaling, source photo permissions, verify search/menu/product/cart/enquiry states, and independently compare the proposed page to the approved concept. Do not add a Buy button or stock solely to make the concept look shoppable.

## Sources and license

Existing identity and exact product photos: Rozmiso active storefront and rozmiso-studio-theme, observed 6 October 2026.
Manrope font: https://github.com/google/fonts/tree/main/ofl/manrope - SIL Open Font License included as FONT-LICENSE.txt.
Functional SVG icon geometry: created for this kit; no third-party icon set copied.
Shopify favicon reference: https://help.shopify.com/en/manual/online-store/images/add-favicon
W3C target sizing: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
''',encoding='utf-8')
print(json.dumps({'logo_variants':len(logos),'functional_icons':len(icons),'mobile_concept':'review only','live_theme_changed':False}))
