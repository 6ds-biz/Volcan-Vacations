import {TourEditor} from '../../../../components/tour-manager';
import {PageAccess} from '../../../../components/page-access';
export default function Page(){return <PageAccess capability="tours.write"><TourEditor/></PageAccess>;}
