from pathlib import Path
import json, hashlib

root = Path('F:/Dropshipping')
output = root / 'team/reports/T035/operations'
manifest = json.loads((root / 'team/reports/T030/catalog-ready/manifest.json').read_text())
corrected = json.loads((root / 'team/reports/T033/MEDIA.json').read_text())
soap_id = '10252037456064'
products = []
problems = []
for product in manifest['products']:
    images = []
    for item in product['images']:
        path = Path(item['path'])
        exists = path.is_file()
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if exists else None
        match = digest == item['sha256']
        images.append({'order':item['order'], 'path':str(path), 'exists':exists, 'sha256MatchesManifest':match})
        if not exists or not match:
            problems.append({'productId':product['productId'], 'path':str(path), 'exists':exists, 'sha256MatchesManifest':match})
    description = Path(product['descriptionHtml'])
    products.append({'productId':product['productId'], 'title':product['title'], 'images':images, 'descriptionExists':description.is_file(), 'uploadState':'HOLD_OBSOLETE_SOAP_MEDIA' if product['productId']==soap_id else 'LOCAL_BYTES_VERIFIED_VISUAL_REVIEW_NOT_REPEATED', 'liveState':'NOT_CHECKED_BY_THIS_LANE'})
replacement = []
for index, item in enumerate(corrected, 1):
    path = root / 'rozmiso-studio-theme/assets' / item['asset']
    exists = path.is_file()
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if exists else None
    replacement.append({'order':index, 'name':item['name'], 'path':str(path), 'exists':exists, 'sha256':digest, 'sha256MatchesT033':digest==item['sha256'], 'recordedReview':item['review']})
result = {
    'date':'2026-10-22',
    'source':'team/reports/T030/catalog-ready/manifest.json',
    'scope':'Local file integrity only. No external upload or visual re-review. Source manifest left unchanged.',
    'products':products,
    'summary':{'products':len(products), 'images':sum(len(p['images']) for p in products), 'fileProblems':problems, 'missingDescriptions':[p['productId'] for p in products if not p['descriptionExists']]},
    'soapCorrection':{'productId':soap_id, 'obsoleteManifestMustNotBeBlindlyUploaded':True, 'replacementSource':'team/reports/T033/MEDIA.json', 'replacementImages':replacement, 'nextAction':'Root to accept overlay into catalog upload plan, verify live product/variant identity and actual saved gallery. This file authorizes no upload.'}
}
(output/'CATALOG-PREFLIGHT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'summary':result['summary'], 'correctedSoapAssetsVerified':sum(i['sha256MatchesT033'] for i in replacement)}))
