import { useState } from "react";
import Map from "../component/MapWrapper";
import MessageSubmit from "../components/MessageSubmit";

const MapPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<any | null>(null);
  const [showMessageSubmit, setShowMessageSubmit] = useState(false);

  // Example markers around Halifax
  const exampleMarkers: Array<[number, number]> = [
    [44.6488, -63.5752], // Halifax Citadel
    [44.65, -63.58], // Halifax Public Gardens
    [44.64, -63.57], // Point Pleasant Park
    [44.655, -63.585], // Halifax Common
    [44.645, -63.59], // Halifax Waterfront
  ];

  // Calculate distance between two points in kilometers
  const calculateDistance = (
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number
  ): number => {
    const R = 6371; // Earth's radius in kilometers
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const handleMapClick = (latlng: any) => {
    // Check if click is near any existing marker (within 0.1km)
    const isNearMarker = exampleMarkers.some((marker) => {
      const distance = calculateDistance(
        latlng.lat,
        latlng.lng,
        marker[0],
        marker[1]
      );
      return distance < 0.1; // 100 meters threshold
    });

    if (isNearMarker) {
      console.log("Clicked near an existing marker!");
      return;
    }

    setSelectedLocation(latlng);
    setShowMessageSubmit(true);
  };

  return (
    <div>
      <Map ClickHandler={handleMapClick} markers={exampleMarkers} />
      <MessageSubmit
        isOpen={showMessageSubmit}
        onClose={() => setShowMessageSubmit(false)}
        location={selectedLocation}
      />
    </div>
  );
};

export default MapPage;
