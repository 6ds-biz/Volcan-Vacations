import type {MediaAsset,MediaProvider} from '@6ds/page-builder/core';
/** Public renderer receives approved public metadata only. The Owner catalog uses a separate endpoint. */
export function publicMediaProvider(assets:MediaAsset[]):MediaProvider{
 const catalog=new Map(assets.map(a=>[a.id,a]));
 return {categories:['Destinations','Tours','General'],list:async(query='',category='')=>assets.filter(a=>(!query||(a.filename+' '+a.alt).toLowerCase().includes(query.toLowerCase()))&&(!category||a.tags?.includes(category))),get:async id=>catalog.get(id)||null,validateSource:a=>catalog.get(a.id)?.source===a.source&&a.rights_status==='APPROVED'&&/^\/images\/[a-zA-Z0-9/_-]+\.(webp|png|jpe?g|avif)$/.test(a.source)};
}
