const fs = require('fs');

const products = [
  {
    handle: "cordless-car-vacuum-air-blower",
    title: "2-in-1 Cordless High-Power Car Vacuum Cleaner & Air Duster",
    body: "<p>Keep your car interior showroom-clean in minutes! High-speed cyclone suction cleans crumbs and dirt, while the reverse air blower cleans AC vents and keyboards.</p><ul><li><b>2-in-1 Dual Function:</b> High-power vacuum + powerful air duster</li><li><b>Rechargeable:</b> USB Type-C fast charging with 45-min battery</li><li><b>Washable HEPA Filter:</b> Reusable and eco-friendly</li><li><b>100% Cash On Delivery Available</b> with Free Shipping</li></ul>",
    vendor: "Rozmiso",
    standardType: "Automotive",
    customType: "Car Gadgets",
    tags: "bestseller,car,gadgets,problem-solver",
    published: "TRUE",
    optionName: "Package",
    variants: [
      {
        optionValue: "1 Unit (Standard Pack)",
        sku: "ROZ-VAC-01",
        grams: "380",
        tracker: "shopify",
        qty: "150",
        policy: "deny",
        fulfillment: "manual",
        price: "999.00",
        comparePrice: "1499.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80"
      },
      {
        optionValue: "2 Units (Car + Home Bundle - Save ₹300!)",
        sku: "ROZ-VAC-02",
        grams: "760",
        tracker: "shopify",
        qty: "100",
        policy: "deny",
        fulfillment: "manual",
        price: "1699.00",
        comparePrice: "2998.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      },
      {
        optionValue: "3 Units (Family Super Bundle - Save ₹700!)",
        sku: "ROZ-VAC-03",
        grams: "1140",
        tracker: "shopify",
        qty: "50",
        policy: "deny",
        fulfillment: "manual",
        price: "2299.00",
        comparePrice: "4497.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      }
    ]
  },
  {
    handle: "ems-acupoint-foot-massager-mat",
    title: "EMS Bio-Electric Acupoint Foot Massager Mat",
    body: "<p>Instant relief from leg pain, heel ache, and varicose veins. Uses gentle bio-electric acupressure impulses to stimulate blood circulation and relieve fatigue after a long workday.</p><ul><li><b>8 Massage Modes & 19 Intensity Levels</b></li><li><b>Foldable & Portable:</b> Roll up and carry anywhere</li><li><b>USB Rechargeable:</b> Lasts for days on a single charge</li><li><b>Safe for daily home therapy</b></li></ul>",
    vendor: "Rozmiso",
    standardType: "Health & Beauty",
    customType: "Wellness",
    tags: "bestseller,health,massage,pain-relief",
    published: "TRUE",
    optionName: "Package",
    variants: [
      {
        optionValue: "1 Piece (Standard Therapy Mat)",
        sku: "ROZ-FOOT-01",
        grams: "160",
        tracker: "shopify",
        qty: "200",
        policy: "deny",
        fulfillment: "manual",
        price: "799.00",
        comparePrice: "1299.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"
      },
      {
        optionValue: "2 Pieces (Self + Parents Care Bundle - Save ₹200!)",
        sku: "ROZ-FOOT-02",
        grams: "320",
        tracker: "shopify",
        qty: "120",
        policy: "deny",
        fulfillment: "manual",
        price: "1399.00",
        comparePrice: "2598.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      }
    ]
  },
  {
    handle: "mini-pocket-thermal-printer",
    title: "Mini Portable Bluetooth Inkless Pocket Printer",
    body: "<p>No ink, no toner, no ribbons needed! Print notes, study diagrams, to-do lists, photos, and shipping labels instantly from your smartphone via Bluetooth.</p><ul><li><b>Zero Ink Technology:</b> High-resolution thermal printing</li><li><b>Compact & Lightweight:</b> Easily fits in your pocket or school bag</li><li><b>Compatible with Android & iPhone</b></li></ul>",
    vendor: "Rozmiso",
    standardType: "Electronics",
    customType: "Gadgets",
    tags: "bestseller,electronics,gadgets,student",
    published: "TRUE",
    optionName: "Package",
    variants: [
      {
        optionValue: "Printer + 1 Free Roll",
        sku: "ROZ-PRN-01",
        grams: "180",
        tracker: "shopify",
        qty: "100",
        policy: "deny",
        fulfillment: "manual",
        price: "1499.00",
        comparePrice: "2199.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=80"
      },
      {
        optionValue: "Printer + 5 Extra Thermal Paper Rolls Bundle",
        sku: "ROZ-PRN-02",
        grams: "280",
        tracker: "shopify",
        qty: "80",
        policy: "deny",
        fulfillment: "manual",
        price: "1899.00",
        comparePrice: "2899.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      }
    ]
  },
  {
    handle: "rechargeable-fabric-shaver-lint-remover",
    title: "USB Rechargeable Electric Fabric Shaver & Lint Remover",
    body: "<p>Make your old woolen sweaters, jackets, shawls, and sofa fabric look brand new in 30 seconds! High-speed 6-blade rotary head gently shaves pills, fuzz, and lint without damaging delicate fabric.</p><ul><li><b>Honeycomb Safety Mesh:</b> Zero fabric snagging</li><li><b>Large Lint Collector Bin:</b> Easy twist-to-empty design</li><li><b>Fast Type-C Charging</b></li></ul>",
    vendor: "Rozmiso",
    standardType: "Home & Kitchen",
    customType: "Home Care",
    tags: "bestseller,cleaning,clothing,home",
    published: "TRUE",
    optionName: "Package",
    variants: [
      {
        optionValue: "1 Unit (Standard Pack)",
        sku: "ROZ-LINT-01",
        grams: "190",
        tracker: "shopify",
        qty: "250",
        policy: "deny",
        fulfillment: "manual",
        price: "799.00",
        comparePrice: "1299.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?auto=format&fit=crop&w=800&q=80"
      },
      {
        optionValue: "2 Units (Home + Office Pack - Save ₹200!)",
        sku: "ROZ-LINT-02",
        grams: "380",
        tracker: "shopify",
        qty: "150",
        policy: "deny",
        fulfillment: "manual",
        price: "1399.00",
        comparePrice: "2598.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      }
    ]
  },
  {
    handle: "astronaut-galaxy-nebula-projector",
    title: "Astronaut 360° Rotating Galaxy Nebula Night Projector",
    body: "<p>Transform your bedroom or living room into a magical starry universe! 8 breathtaking dynamic nebula colors with twinkling green laser stars. Features a 360-degree magnetic rotating astronaut head and wireless remote control.</p><ul><li><b>8 Nebula Effects with Timer Mode</b></li><li><b>Remote Control Included</b></li><li><b>The Ultimate Birthday & Festive Gift</b></li></ul>",
    vendor: "Rozmiso",
    standardType: "Home & Living",
    customType: "Decor",
    tags: "bestseller,decor,gift,kids",
    published: "TRUE",
    optionName: "Package",
    variants: [
      {
        optionValue: "1 Piece (Astronaut Projector)",
        sku: "ROZ-ASTRO-01",
        grams: "320",
        tracker: "shopify",
        qty: "90",
        policy: "deny",
        fulfillment: "manual",
        price: "1099.00",
        comparePrice: "1799.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?auto=format&fit=crop&w=800&q=80"
      },
      {
        optionValue: "2 Pieces (Bedroom + Gift Bundle - Save ₹300!)",
        sku: "ROZ-ASTRO-02",
        grams: "640",
        tracker: "shopify",
        qty: "60",
        policy: "deny",
        fulfillment: "manual",
        price: "1899.00",
        comparePrice: "3598.00",
        reqShipping: "TRUE",
        taxable: "TRUE",
        image: ""
      }
    ]
  }
];

function escapeCSV(val) {
  if (val === undefined || val === null) return '';
  const str = String(val);
  if (str.includes(',') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

const headers = [
  'Handle',
  'Title',
  'Body (HTML)',
  'Vendor',
  'Standard Product Type',
  'Custom Product Type',
  'Tags',
  'Published',
  'Option1 Name',
  'Option1 Value',
  'Variant SKU',
  'Variant Grams',
  'Variant Inventory Tracker',
  'Variant Inventory Qty',
  'Variant Inventory Policy',
  'Variant Fulfillment Service',
  'Variant Price',
  'Variant Compare At Price',
  'Variant Requires Shipping',
  'Variant Taxable',
  'Image Src',
  'Status'
];

const rows = [headers.map(escapeCSV).join(',')];

for (const p of products) {
  p.variants.forEach((v, idx) => {
    const isFirst = idx === 0;
    const row = [
      p.handle,
      isFirst ? p.title : '',
      isFirst ? p.body : '',
      isFirst ? p.vendor : '',
      isFirst ? p.standardType : '',
      isFirst ? p.customType : '',
      isFirst ? p.tags : '',
      isFirst ? p.published : '',
      p.optionName,
      v.optionValue,
      v.sku,
      v.grams,
      v.tracker,
      v.qty,
      v.policy,
      v.fulfillment,
      v.price,
      v.comparePrice,
      v.reqShipping,
      v.taxable,
      v.image,
      'active'
    ];
    if (row.length !== headers.length) {
      throw new Error(`Row length mismatch: ${row.length} vs ${headers.length}`);
    }
    rows.push(row.map(escapeCSV).join(','));
  });
}

const csvOutput = rows.join('\r\n');
fs.writeFileSync('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv', csvOutput, 'utf8');
console.log('Successfully generated valid CSV with ' + (rows.length - 1) + ' rows and ' + headers.length + ' columns per row!');
