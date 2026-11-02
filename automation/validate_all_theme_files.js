const { execSync } = require('child_process');
const path = require('path');

const files = [
  'layout/theme.liquid',
  'sections/announcement-bar.liquid',
  'sections/customer-reviews.liquid',
  'sections/faq-section.liquid',
  'sections/featured-collection.liquid',
  'sections/footer.liquid',
  'sections/header.liquid',
  'sections/hero-banner.liquid',
  'sections/main-product.liquid',
  'sections/trust-badges.liquid'
];

for (const rel of files) {
  const full = path.resolve('f:/Dropshipping/rozmiso-shopify-store/' + rel);
  const name = path.basename(rel);
  try {
    const cmd = `node C:/Users/Abhinand/.gemini/config/plugins/shopify-ai-toolkit/skills/shopify/scripts/validate.mjs --api liquid --filename ${name} --file "${full}"`;
    const res = execSync(cmd, { encoding: 'utf8' });
    console.log(name, res.includes('SUCCESS') ? '✅ PASS' : '⚠️ ' + res.trim());
  } catch (err) {
    console.log(name, '❌ FAILED:', err.stdout || err.message);
  }
}
