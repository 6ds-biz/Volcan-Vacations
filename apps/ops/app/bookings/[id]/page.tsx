import { BookingDetail } from '../../../components/booking-manager';
export default async function BookingPage({params}: {params: Promise<{id: string}>}) { return <BookingDetail id={(await params).id} />; }
