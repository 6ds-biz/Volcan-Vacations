import {SupplierEditor} from '../../../../components/supplier-manager';
import {PageAccess} from '../../../../components/page-access';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;return <PageAccess capability="suppliers.read"><SupplierEditor id={id}/></PageAccess>;}
