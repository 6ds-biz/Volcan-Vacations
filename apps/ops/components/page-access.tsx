'use client';
import Link from 'next/link';
import {useIdentity} from './ops-ui';
export function PageAccess({capability,children}:{capability:string;children:React.ReactNode}){const user=useIdentity();return user.permissions.includes(capability)?<>{children}</>:<section className="restricted"><h1>Access restricted</h1><p>Your role does not include this workspace.</p><Link href="/">Return to your dashboard</Link></section>;}
