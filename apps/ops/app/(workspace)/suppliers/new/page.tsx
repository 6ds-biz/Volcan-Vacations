import {SupplierEditor} from '../../../../components/supplier-manager';
import {PageAccess} from '../../../../components/page-access';
export default function Page(){return <PageAccess capability="suppliers.write"><SupplierEditor/></PageAccess>;}
