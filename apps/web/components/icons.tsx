import type { SVGProps } from 'react';

type IconProps = SVGProps<SVGSVGElement>;
const shared = { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.7, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, 'aria-hidden': true };

export function ArrowIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M5 12h14M14 7l5 5-5 5" /></svg>; }
export function ClockIcon(props: IconProps) { return <svg {...shared} {...props}><circle cx="12" cy="12" r="8.5" /><path d="M12 7.5V12l3 2" /></svg>; }
export function LeafIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M19.5 4.5C12 4.2 6 7.5 5 13.3c-.5 3 1.6 5.2 4.4 4.7 5.7-1 8.9-6.7 10.1-13.5Z" /><path d="M4 20c2.8-4.2 6.6-7.4 11.4-9.7" /></svg>; }
export function CompassIcon(props: IconProps) { return <svg {...shared} {...props}><circle cx="12" cy="12" r="9" /><path d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9 4.9-2.1Z" /></svg>; }
export function SparkIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M12 3c.8 4.8 3.2 7.2 8 8-4.8.8-7.2 3.2-8 8-.8-4.8-3.2-7.2-8-8 4.8-.8 7.2-3.2 8-8Z" /></svg>; }
export function HeartIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M20 8.8c0 5.1-8 10-8 10s-8-4.9-8-10a4.3 4.3 0 0 1 7.7-2.6l.3.4.3-.4A4.3 4.3 0 0 1 20 8.8Z" /></svg>; }
export function MailIcon(props: IconProps) { return <svg {...shared} {...props}><rect x="3" y="5" width="18" height="14" rx="2" /><path d="m4 7 8 6 8-6" /></svg>; }
export function MapPinIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M20 10c0 5.4-8 11-8 11S4 15.4 4 10a8 8 0 1 1 16 0Z" /><circle cx="12" cy="10" r="2.5" /></svg>; }
export function MountainIcon(props: IconProps) { return <svg {...shared} {...props}><path d="m2 20 8-15 4 7 3-5 5 13H2Z" /><path d="m7.5 10 2.5 2 2.5-2M15.5 10l2 2 1-1" /></svg>; }
export function CupIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M4 7h13v6a6.5 6.5 0 0 1-13 0V7ZM17 8h2a3 3 0 0 1 0 6h-2M3 21h16M8 2v2M13 2v2" /></svg>; }
export function RequestIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M5 2h9l5 5v15H5V2ZM14 2v6h5M9 12h6M9 16h6" /></svg>; }
export function CalendarIcon(props: IconProps) { return <svg {...shared} {...props}><rect x="3" y="5" width="18" height="17" rx="2" /><path d="M7 2v6M17 2v6M3 10h18M7 14h1M12 14h1M17 14h1M7 18h1M12 18h1" /></svg>; }
export function PalmIcon(props: IconProps) { return <svg {...shared} {...props}><path d="M11 21c2-5 2-10 1-15M7 22h12M12 6C8 1 3 3 2 7c4-2 7-2 10-1ZM12 6c3-5 8-4 10 0-4-1-7-1-10 0ZM12 6c-5-1-8 3-7 7 2-3 4-5 7-7ZM12 6c5 0 7 3 6 7-2-3-3-5-6-7Z" /></svg>; }
