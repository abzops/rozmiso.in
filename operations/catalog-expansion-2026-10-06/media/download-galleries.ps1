$ErrorActionPreference='Stop'
$base='F:/Dropshipping/operations/catalog-expansion-2026-10-06/media'
$records=Get-Content 'F:/Dropshipping/operations/product-media-2026-10-06/media-manifest.json' -Raw|ConvertFrom-Json
$map=@{
 '23469_electric_lint_remover_1pc_no5'='usb-rechargeable-fabric-shaver'
 '6329_5in1_magic_cleaning_brush'='5-in-1-rechargeable-cleaning-brush'
 '0642_multipurpose_travel_organizer_bag_1pc_no1'='everyday-travel-organizer-pouch'
 '22895_plastic_2in1_soap_dispenser_cleaning_brush'='2-in-1-soap-dispensing-cleaning-brush'
}
$out=@()
foreach($r in $records){
 $handle=$map[$r.sku]
 if(-not $handle){throw 'Unknown SKU'}
 $dir=Join-Path $base $handle
 New-Item -ItemType Directory -Force $dir|Out-Null
 $path=Join-Path $dir ('supplier-'+('{0:D2}' -f [int]$r.position)+'.jpg')
 if(-not(Test-Path -LiteralPath $path)){Invoke-WebRequest -Uri $r.url -OutFile $path}
 $item=Get-Item -LiteralPath $path
 $alt=$r.alt
 if(-not $alt){$alt='Supplier catalog image of '+$handle.Replace('-',' ')}
 $out += [pscustomobject]@{
   store_handle=$handle;supplier_sku=$r.sku;position=$r.position;local_path=$path.Replace('\','/');filename=$item.Name;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash;alt=$alt;source_url=$r.url;source_page=$r.source_page;source_media_id=$r.source_media_id;source_type='supplier_catalog_image';capture_provenance='unverified; may include staged or generated illustration';rights=$r.rights;user_copy_authorized='T017 explicit request; this is not a supplier license';supplier_permission_obtained=$false;exact_physical_model_verified=$false;generated_by_this_task=$false
 }
}
$out|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $base 'gallery.json')
Write-Output ('Downloaded/indexed '+$out.Count+' images; '+($out|Measure-Object bytes -Sum).Sum+' bytes')
