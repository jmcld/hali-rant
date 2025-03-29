import { useState } from "react";
import Map from "../component/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<any | null>(null);
  const [showMessageSubmit, setShowMessageSubmit] = useState(false);

  const handleMapClick = (latlng: any) => {
    setSelectedLocation(latlng);
    setShowMessageSubmit(true);
  };

  return (
    <div>
      <Map ClickHandler={handleMapClick} />
      <MessageSubmit
        isOpen={showMessageSubmit}
        onClose={() => setShowMessageSubmit(false)}
        location={selectedLocation}
      />
    </div>
  );
};

export default MapPage;
