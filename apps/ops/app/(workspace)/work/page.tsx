import {WorkList} from '../../../components/work';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="bookings.read_assigned"><WorkList/></PageAccess>;}
