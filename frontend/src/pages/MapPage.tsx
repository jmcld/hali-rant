import { useEffect, useState } from "react";
import Map from "../components/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";
import AddButton from "../components/AddButton";
import RepliesModal from "../components/RepliesModal";
import { Marker } from "../types";
import { exampleMarkers as initialMarkers } from "../fake-db";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<any | null>(null);
  const [showMessageSubmit, setShowMessageSubmit] = useState(false);
  const [addRant, setAddRant] = useState(false);
  const [showRepliesModal, setShowRepliesModal] = useState(false);
  const [selectedMarker, setSelectedMarker] = useState<Marker | null>(null);
  const [exampleMarkers, setExampleMarkers] =
    useState<Array<Marker>>(initialMarkers);

  useEffect(() => console.log(selectedLocation), [selectedLocation]);

  const handleMapClick = (latlng: any) => {
    if (addRant) {
      setSelectedLocation(latlng);
      setShowMessageSubmit(true);
    }
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

  const handleShowReplies = (marker: Marker) => {
    setSelectedMarker(marker);
    setShowRepliesModal(true);
  };

  return (
    <div>
      <Map
        ClickHandler={handleMapClick}
        LikeHandler={handleLike}
        DislikeHandler={handleDislike}
        ShowRepliesHandler={handleShowReplies}
        markers={exampleMarkers}
        addRant={addRant}
      />
      <MessageSubmit
        isOpen={showMessageSubmit}
        onClose={() => {
          setShowMessageSubmit(false);
          setAddRant(false);
        }}
        location={selectedLocation}
      />
      <RepliesModal
        isOpen={showRepliesModal}
        onClose={() => {
          setShowRepliesModal(false);
          setSelectedMarker(null);
        }}
        marker={selectedMarker}
      />
      <AddButton isActive={addRant} onClick={() => setAddRant(!addRant)} />
    </div>
  );
};

export default MapPage;
