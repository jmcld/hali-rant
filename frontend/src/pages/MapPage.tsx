import { useEffect, useState } from "react";
import Map from "../components/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";
import { Marker } from "../types";
import { exampleMarkers as initialMarkers } from "../fake-db";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<any | null>(null);
  const [showMessageSubmit, setShowMessageSubmit] = useState(false);
  const [exampleMarkers, setExampleMarkers] =
    useState<Array<Marker>>(initialMarkers);

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
