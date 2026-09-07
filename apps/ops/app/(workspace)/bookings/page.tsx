import {BookingsList} from '../../../components/business-lists';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="bookings.read"><BookingsList/></PageAccess>;}
