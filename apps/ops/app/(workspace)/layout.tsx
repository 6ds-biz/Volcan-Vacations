import {redirect} from 'next/navigation';
import {session} from '../../lib/server-session';
import {OpsShell} from '../../components/ops-shell';
export const dynamic='force-dynamic';
export default async function Workspace({children}:{children:React.ReactNode}) {const user=await session();if(!user)redirect('/login');if(user.must_change_password)redirect('/change-password');return <OpsShell user={user}>{children}</OpsShell>;}
