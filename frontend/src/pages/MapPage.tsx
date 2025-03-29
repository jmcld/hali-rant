import { useEffect, useState } from "react";
import Map from "../components/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";
import { Marker } from "../types";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<any | null>(null);
  const [showMessageSubmit, setShowMessageSubmit] = useState(false);

  // Example markers around Halifax
  const [exampleMarkers, setExampleMarkers] = useState<Array<Marker>>([
    {
      id: "0",
      title: "Halifax Citadel",
      body: "The Halifax Citadel is a historic fortification in Halifax, Nova Scotia. It was built in the 18th century to protect the city from potential attacks.",
      location: { lat: 44.6488, lng: -63.5752 },
      likes: 0,
      dislikes: 0,
    },
    {
      id: "1",
      title: "Halifax Public Gardens",
      body: "The Halifax Public Gardens is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
      location: { lat: 44.65, lng: -63.58 },
      likes: 0,
      dislikes: 0,
    },
    {
      id: "2",
      title: "Point Pleasant Park",
      body: "Point Pleasant Park is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
      location: { lat: 44.64, lng: -63.57 },
      likes: 0,
      dislikes: 0,
    },
    {
      id: "3",
      title: "Halifax Common",
      body: "The Halifax Common is a beautiful park in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
      location: { lat: 44.645, lng: -63.59 },
      likes: 0,
      dislikes: 0,
    },
    {
      id: "4",
      title: "Halifax Waterfront",
      body: "The Halifax Waterfront is a beautiful waterfront in Halifax, Nova Scotia. It is a popular spot for locals and tourists alike.",
      location: { lat: 44.645, lng: -63.59 },
      likes: 0,
      dislikes: 0,
    },
  ]);

  useEffect(() => console.log(selectedLocation), [selectedLocation]);

  const handleMapClick = (latlng: any) => {
    setSelectedLocation(latlng);
    setShowMessageSubmit(true);
  };

  const handleLike = (marker: Marker) => {
    setExampleMarkers((prevMarkers: Array<Marker>) =>
      prevMarkers.map((m) =>
        m.id === marker.id ? { ...m, likes: m.likes + 1 } : m
      )
    );
  };

  const handleDislike = (marker: Marker) => {
    setExampleMarkers((prevMarkers: Array<Marker>) =>
      prevMarkers.map((m) =>
        m.id === marker.id ? { ...m, dislikes: m.dislikes + 1 } : m
      )
    );
  };

  return (
    <div>
      <Map
        ClickHandler={handleMapClick}
        LikeHandler={handleLike}
        DislikeHandler={handleDislike}
        markers={exampleMarkers}
      />
      <MessageSubmit
        isOpen={showMessageSubmit}
        onClose={() => setShowMessageSubmit(false)}
        location={selectedLocation}
      />
    </div>
  );
};

export default MapPage;
