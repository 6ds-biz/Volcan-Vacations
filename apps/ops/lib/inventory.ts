export type Supplier = {
  id: number; name: string; supplier_type: string; contact_name: string | null;
  email: string | null; phone: string | null; website: string | null;
  notes: string | null; active: boolean;
};
export type ProductImage = {id: number; image_url: string; alt_text: string; sort_order: number; is_primary: boolean};
export type Tour = {
  id: number; supplier_id: number; supplier: Supplier; name: string; slug: string;
  short_description: string; description: string | null; product_type: 'tour';
  category: string; duration: string; location: string | null; difficulty: string | null;
  minimum_age: number | null; retail_price: string; supplier_cost: string;
  gross_margin: string; active: boolean; featured: boolean;
  primary_image: ProductImage | null; images: ProductImage[];
};

// Decimal text and integer cents only; never floating-point money arithmetic.
export function margin(retail: string, cost: string): string {
  const cents = (value: string) => {
    if (!/^\d+(\.\d{1,2})?$/.test(value)) throw new Error('Invalid price');
    const [whole, fraction = ''] = value.split('.');
    return BigInt(whole) * BigInt(100) + BigInt(fraction.padEnd(2, '0'));
  };
  try {
    const value = cents(retail) - cents(cost);
    const absolute = value < BigInt(0) ? -value : value;
    return `${value < BigInt(0) ? '-' : ''}${absolute / BigInt(100)}.${String(absolute % BigInt(100)).padStart(2, '0')}`;
  } catch { return '—'; }
}
