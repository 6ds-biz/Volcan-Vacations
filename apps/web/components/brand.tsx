import Link from 'next/link';

// The original PNG supplies the complete logo silhouette; CSS only colors it.
export function Brand() {
  return (
    <Link className="brand" href="/" aria-label="Volcan Vacations home">
      <span className="brand__logo" aria-hidden="true" />
      <span className="brand__tagline">Explore · Experience · Belong</span>
    </Link>
  );
}
