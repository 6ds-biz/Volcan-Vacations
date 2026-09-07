import type {Metadata} from 'next';
import {Container} from '../../components/ui';
import {PaymentCheckout} from '../../components/payment-checkout';
import './payment.css';

export const metadata: Metadata = {title: 'Your Tour Payment', robots: {index: false, follow: false}, referrer: 'no-referrer'};
export default function PaymentPage() {
  return <main id="main-content" className="section vv-payment-page"><Container><PaymentCheckout /></Container></main>;
}
