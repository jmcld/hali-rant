export interface Marker {
  id: string;
  title: string;
  body: string;
  location: { lat: number; lng: number };
  likes: number;
  dislikes: number;
  replies: string[];
  category: string;
}