import {Profile} from '../../../components/records';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="settings.read"><Profile settings/></PageAccess>;}
