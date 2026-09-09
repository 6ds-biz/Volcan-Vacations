import {ScenicImage} from '../../../../web/components/scenic-image';

/** Build-time substitution for VV inventory and availability; no network calls. */
export function TourInventory({limit = 3}: {featured?: boolean; filters?: boolean; limit?: number}) {
  return <div><p className="builder-sample-note" role="note">Sample inventory · layout preview only</p><div className="tour-grid">{[
    ['Rainforest discovery', '/images/rainforest.webp', 'A guided walk beneath the canopy.'],
    ['Arenal adventure', '/images/arenal.webp', 'Explore the landscape around the volcano.'],
    ['A quiet coastal escape', '/images/coast/papagayo-temporary.webp', 'Make space for ocean views and a slower pace.'],
  ].slice(0, limit).map(([name, src, copy]) => <article className="tour-card" key={name}><div className="tour-card__image"><ScenicImage src={src} alt={name}/></div><div className="tour-card__body"><p className="eyebrow">Costa Rica · Sample experience</p><h3>{name}</h3><p>{copy}</p><span>Request details →</span></div></article>)}</div></div>;
}
export function TourAvailability() {
  return <div className="builder-sample-note"><p>Availability placement · application widget</p><p>Date selection and availability are supplied by the public application.</p></div>;
}
