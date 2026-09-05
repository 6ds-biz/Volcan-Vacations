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
