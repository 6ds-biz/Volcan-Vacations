export type Contact = {first_name: string; last_name: string; email: string; phone: string | null; preferred_contact_method: string | null};
export type Booking = {
  id: number; reference: string; status: string; allowed_statuses: string[]; created_at: string; updated_at: string;
  tour_name: string; product_id: number; requested_date: string; requested_time: string | null; quantity: number;
  unit_price: string; supplier_unit_cost: string; retail_total: string; gross_margin: string;
  customer: Contact & {id: number; notes: string | null}; submitted_contact: Contact | null;
  travelers: {id: number; first_name: string; last_name: string; traveler_type: string | null; date_of_birth: string | null}[];
  trip: {id: number; reference: string; name: string | null; start_date: string | null; end_date: string | null; party_size: number; status: string; notes: string | null};
  customer_notes: string | null; internal_notes: string | null;
};
export const bookingStatuses = ['new', 'contacted', 'pending_supplier', 'confirmed', 'cancelled', 'completed'];
export const statusLabel = (status: string) => status.replace(/_/g, ' ').replace(/^./, character => character.toUpperCase());
