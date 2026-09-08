import Link from 'next/link';
import type {MediaConfig} from '@6ds/page-builder/core';
import {ConfiguredMedia} from './website/public-media';
import type { ReactNode } from 'react';
import { ArrowIcon } from './icons';
import { ScenicImage } from './scenic-image';

export function Container({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`container ${className}`.trim()}>{children}</div>;
}

export function LinkButton({ href, children, variant = 'primary', arrow = false }: { href: string; children: ReactNode; variant?: 'primary' | 'secondary' | 'light' | 'text'; arrow?: boolean }) {
  return <Link className={`button button--${variant}`} href={href}>{children}{arrow ? <ArrowIcon width={18} height={18} /> : null}</Link>;
}

export function Eyebrow({ children }: { children: ReactNode }) { return <p className="eyebrow">{children}</p>; }

export function SectionHeading({ eyebrow, title, intro, align = 'left' }: { eyebrow?: string; title: string; intro?: string; align?: 'left' | 'center' }) {
  return <div className={`section-heading section-heading--${align}`}>{eyebrow ? <Eyebrow>{eyebrow}</Eyebrow> : null}<h2>{title}</h2>{intro ? <p>{intro}</p> : null}</div>;
}

export function PageHero({ eyebrow, title, intro, media, subheadline, className='' }: { eyebrow: string; title: string; intro: string; media?:MediaConfig; subheadline?:string; className?:string }) {
  return <section className={`page-hero ${className}`} >{media?<ConfiguredMedia config={media} scenic/>:<ScenicImage priority />}<Container><div className="page-hero__content"><Eyebrow>{eyebrow}</Eyebrow><h1>{title}</h1>{subheadline&&<p className="website-subheadline">{subheadline}</p>}<p>{intro}</p></div></Container></section>;
}
