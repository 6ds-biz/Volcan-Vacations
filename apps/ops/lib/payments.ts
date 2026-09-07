export type Payment = {
  id: number; reservation_id: number | null; trip_id: number; booking_reference: string;
  customer: string; tour: string; amount: string; currency: string; status: string; provider: string;
  provider_environment: string | null; provider_order_id: string | null; provider_capture_id: string | null;
  external_reference: string | null; failure_code: string | null; failure_message: string | null;
  reconciliation_required: boolean; created_at: string; updated_at: string; paid_at: string | null; refunded_amount: string;
};
export type BookingPayment = {
  eligible: boolean; label: string; amount_due: string; currency: string;
  payment_due_at: string | null; overdue: boolean; link_active: boolean;
  sandbox_configured: boolean; webhook_configured: boolean; payment: Payment | null;
};
