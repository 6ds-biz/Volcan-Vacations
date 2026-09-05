import Image from 'next/image';

export function ScenicImage({ src = '/images/arenal.webp', alt = '', priority = false, sizes = '100vw' }: { src?: string; alt?: string; priority?: boolean; sizes?: string }) {
  return <Image className="scenic-image" src={src} alt={alt} fill sizes={sizes} priority={priority} />;
}
