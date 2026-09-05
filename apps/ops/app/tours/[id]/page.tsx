import { TourEditor } from '../../../components/tour-manager';
export default async function TourPage({params}: {params: Promise<{id: string}>}) { return <TourEditor id={(await params).id} />; }
