import {TourEditor} from '../../../../components/tour-manager';
import {PageAccess} from '../../../../components/page-access';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;return <PageAccess capability="tours.read"><TourEditor id={id}/></PageAccess>;}
