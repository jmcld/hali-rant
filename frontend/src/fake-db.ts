import { Marker } from "./types";

export const exampleMarkers: Array<Marker> = [
  {
    id: "0",
    title: "Halifax Citadel",
    body: "The Halifax Citadel is a historic fortification in Halifax, Nova Scotia. It was built in the 18th century to protect the city from potential attacks.",
    location: { lat: 44.6488, lng: -63.5752 },
    likes: 0,
    dislikes: 0,
    replies: [
      "Great historical site!",
      "The guided tours are amazing",
      "Perfect for a picnic with a view",
    ],
    category: "pothole"
  },
  {
    id: "1",
    title: "Halifax Public Gardens",
    body: "The Halifax Public Gardens is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
    location: { lat: 44.65, lng: -63.58 },
    likes: 0,
    dislikes: 0,
    replies: ["Beautiful in the spring!", "Love the Victorian-era design"],
    category: "pothole",
  },
  {
    id: "2",
    title: "Point Pleasant Park",
    body: "Point Pleasant Park is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
    location: { lat: 44.64, lng: -63.57 },
    likes: 0,
    dislikes: 0,
    replies: ["Great for hiking", "Perfect beach access"],
    category: "out-of-order",
  },
  {
    id: "3",
    title: "Halifax Common",
    body: "The Halifax Common is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
    location: { lat: 44.645, lng: -63.59 },
    likes: 0,
    dislikes: 0,
    replies: ["Great for sports", "Nice open space"],
    category: "pothole",
  },
  {
    id: "4",
    title: "Halifax Waterfront",
    body: "The Halifax Waterfront is a beautiful waterfront in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
    location: { lat: 44.645, lng: -63.59 },
    likes: 0,
    dislikes: 0,
    replies: [
      "Amazing restaurants",
      "Beautiful sunset views",
      "Great for walking",
    ],
    category: "red",
  },
]; 