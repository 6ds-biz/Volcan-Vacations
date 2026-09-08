import {TransportationDetail} from '../../../../../components/transportation';
import {PageAccess} from '../../../../../components/page-access';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;return <PageAccess capability="transport.read"><TransportationDetail id={Number(id)}/></PageAccess>;}
