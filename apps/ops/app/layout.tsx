import './globals.css';
import type {Metadata} from 'next';
export const metadata:Metadata={title:'Volcan Vacations Operations',description:'Internal Volcan Vacations Operations.',robots:{index:false,follow:false}};
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>;}
