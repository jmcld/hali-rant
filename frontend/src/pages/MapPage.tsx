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
  const [selectedMarkerID, setSelectedMarkerID] = useState<string | null>(null);
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
    setSelectedMarkerID(marker.id);
    setShowRepliesModal(true);
  };

  const handleAddReply = (markerId: string, reply: string) => {
    setExampleMarkers((prevMarkers: Array<Marker>) =>
      prevMarkers.map((m) =>
        m.id === markerId ? { ...m, replies: [...(m.replies || []), reply] } : m
      )
    );
  };

  const handleAddMarker = (marker: {
    title: string;
    body: string;
    location: { lat: number; lng: number };
    category: string;
  }) => {
    const newMarker: Marker = {
      ...marker,
      id: Math.random().toString(),
      likes: 0,
      dislikes: 0,
      replies: [],
    };

    setExampleMarkers((prevMarkers: Array<Marker>) => [
      ...prevMarkers,
      newMarker,
    ]);
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
        addMarker={handleAddMarker}
      />
      <RepliesModal
        isOpen={showRepliesModal}
        onClose={() => {
          setShowRepliesModal(false);
          setSelectedMarkerID(null);
        }}
        selectedMarkerID={selectedMarkerID}
        markers={exampleMarkers}
        onAddReply={handleAddReply}
      />
      <AddButton isActive={addRant} onClick={() => setAddRant(!addRant)} />
    </div>
  );
};

export default MapPage;
