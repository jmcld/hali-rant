import { useState } from "react";
import Map from "../components/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<
    [number, number] | null
  >(null);
  const [showModal, setShowModal] = useState(false);

  const handleMapClick = (latlng: any) => {
    setSelectedLocation(latlng);
    setShowModal(true);
  };

  return (
    <div>
      <Map ClickHandler={handleMapClick} />
      <MessageSubmit isOpen={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
};

export default MapPage;
