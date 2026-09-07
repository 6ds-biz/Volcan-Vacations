import {redirect} from 'next/navigation';
import Link from 'next/link';
import {session} from '../../lib/server-session';
import {AuthForm} from '../../components/auth-controls';
export default async function ChangePassword(){if(!await session())redirect('/login');return <main className="login-main"><div className="login-panel"><span className="vv-logo" role="img" aria-label="Volcan Vacations"/><h1>Change password</h1><p>Changing your password signs out all sessions.</p><AuthForm change/><p><Link href="/profile">Return to profile</Link></p></div></main>;}
