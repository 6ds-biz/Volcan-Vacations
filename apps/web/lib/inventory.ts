export type ProductImage = {
  id: number;
  image_url: string;
  alt_text: string;
  sort_order: number;
  is_primary: boolean;
};

export type Tour = {
  name: string;
  slug: string;
  short_description: string;
  description: string | null;
  category: string;
  duration: string;
  retail_price: string;
  featured: boolean;
  location: string | null;
  difficulty: string | null;
  minimum_age: number | null;
  primary_image: ProductImage | null;
  images: ProductImage[];
};
