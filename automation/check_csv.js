const fs = require('fs');

function parseCSVLine(text) {
  const result = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (inQuotes && text[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      result.push(cur);
      cur = '';
    } else {
      cur += c;
    }
  }
  result.push(cur);
  return result;
}

const lines = fs.readFileSync('f:/Dropshipping/rozmiso-shopify-store/rozmiso_products.csv', 'utf8').trim().split(/\r?\n/);
const header = parseCSVLine(lines[0]);
console.log('Header (' + header.length + ' cols):', header);

for (let r = 1; r < lines.length; r++) {
  const row = parseCSVLine(lines[r]);
  console.log(`Row ${r}: cols=${row.length}, Price=${row[16]}, CompareAt=${row[17]}, RequiresShipping=${row[18]}`);
  if (row.length !== header.length) {
    console.error(`Mismatch in row ${r}: got ${row.length}, expected ${header.length}`);
  }
}
