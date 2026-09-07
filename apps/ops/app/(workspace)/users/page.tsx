import {UsersPage} from '../../../components/users';
import {PageAccess} from '../../../components/page-access';
export default function Page(){return <PageAccess capability="users.manage"><UsersPage/></PageAccess>;}
