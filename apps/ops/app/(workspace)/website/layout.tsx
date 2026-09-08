import {session} from '../../../lib/server-session';
export default async function WebsiteManagement({children}:{children:React.ReactNode}){const user=await session();if(user?.role!=='owner_admin')return <p role="alert">Website management is available only to the Owner.</p>;return children;}
