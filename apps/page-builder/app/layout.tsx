import '../../web/app/globals.css';
import '../../web/app/home.css';
import '../../web/components/website/editor/editor.css';
import './builder.css';
import type {Metadata} from 'next';
export const metadata: Metadata = {title: '6DS Web Builder', robots: {index: false, follow: false}};
export default function Layout({children}: {children: React.ReactNode}) {
  return <html lang="en"><body>{children}</body></html>;
}
