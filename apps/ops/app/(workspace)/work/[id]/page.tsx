import {WorkDetail} from '../../../../components/work';
import {PageAccess} from '../../../../components/page-access';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;return <PageAccess capability="bookings.read_assigned"><WorkDetail id={id}/></PageAccess>;}
