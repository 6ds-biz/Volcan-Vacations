import { SupplierEditor } from '../../../components/supplier-manager';
export default async function SupplierPage({params}: {params: Promise<{id: string}>}) { return <SupplierEditor id={(await params).id} />; }
