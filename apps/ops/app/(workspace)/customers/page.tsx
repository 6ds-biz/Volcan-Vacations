import {Customers} from '../../../components/records';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="customers.read"><Customers/></PageAccess>;}
