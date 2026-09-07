import {AvailabilityManager} from '../../../components/availability-manager';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="availability.read"><AvailabilityManager/></PageAccess>;}
