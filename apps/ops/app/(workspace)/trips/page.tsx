import {Trips} from '../../../components/records';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="trips.read"><Trips/></PageAccess>;}
