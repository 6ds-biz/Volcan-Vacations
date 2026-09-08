import './globals.css';
import {cookies} from 'next/headers';
import {session} from '../lib/server-session';
import {AppearanceProvider,Appearance} from '../components/appearance';
import type {Metadata} from 'next';
export const metadata:Metadata={title:'Volcan Vacations Operations',description:'Internal Volcan Vacations Operations.',robots:{index:false,follow:false}};
export default async function RootLayout({children}:{children:React.ReactNode}) {
 const user=await session();const cached=(await cookies()).get('vv_ops_appearance')?.value;
 const appearance:Appearance=user?.appearance||(['light','dark','system'].includes(cached||'')?cached as Appearance:'dark');
 return <html lang="en" data-theme={appearance==='system'?'dark':appearance} suppressHydrationWarning><head>{appearance==='system'&&<script dangerouslySetInnerHTML={{__html:"document.documentElement.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'"}}/>}</head><body><AppearanceProvider initial={appearance}>{children}</AppearanceProvider></body></html>;
}
