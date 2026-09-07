export const availabilityStatuses = ['unknown', 'available', 'limited', 'unavailable', 'closed'];
export type Availability = {
  id: number; product_id: number; tour_name: string; supplier_id: number; supplier_name: string;
  date: string; status: string; source: string; capacity: number | null; remaining_capacity: number | null;
  notes: string | null; last_checked_at: string | null; stale: boolean; version: number;
  created_at: string; updated_at: string;
};
export type SupplierEvent = {
  actor_user_id: number | null; actor_display_name: string | null;
  id: number; supplier_id: number; event_type: string; contact_method: string | null;
  operator_identifier: string | null; status: string; reservation_status: string; availability_status: string;
  reference: string | null; notes: string | null; alternative_product_id: number | null;
  alternative_tour_name: string | null; alternative_date: string | null; alternative_time: string | null;
  occurred_at: string; created_at: string;
};
export const localDateTime = (value = new Date().toISOString()) => {
  const date = new Date(value);
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
};
export const timeLabel = (value: string | null) => value ? new Date(value).toLocaleString() : 'Not checked';
