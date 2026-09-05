'use client';

import { useState } from 'react';
import type { ProductImage } from '../lib/inventory';

export function TourPhoto({ image }: { image: ProductImage | null }) {
  const [failedUrl, setFailedUrl] = useState<string | null>(null);
  if (!image || failedUrl === image.image_url) return <span className="tour-photo-placeholder">Photo coming soon</span>;
  // Content URLs render directly in the browser, never through a server-side
  // image proxy that could fetch an operator-supplied internal-network address.
  // eslint-disable-next-line @next/next/no-img-element
  return <img className="scenic-image tour-photo" src={image.image_url} alt={image.alt_text} loading="lazy" decoding="async" referrerPolicy="no-referrer" onError={() => setFailedUrl(image.image_url)} />;
}
