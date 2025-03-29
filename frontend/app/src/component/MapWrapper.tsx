import { MapContainer, TileLayer, useMapEvents } from "react-leaflet";

import "leaflet/dist/leaflet.css";
import styled from "styled-components";

const MapWrapper = styled.div`
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
`;

const Map = (props: { ClickHandler: (latlng: any) => void }) => {
  // Halifax coordinates
  const defaultCenter = [44.6488, -63.5752];
  const defaultZoom = 13;

  const MapClickHandler = () => {
    useMapEvents({
      click: (e) => {
        props.ClickHandler(e.latlng);
      },
    });
    return null;
  };

  // Halifax region bounds
  const bounds = [
    [44.5, -63.8], // Southwest coordinates
    [44.8, -63.3], // Northeast coordinates
  ];

  return (
    <div>
      <MapWrapper>
        <MapContainer
          center={defaultCenter as [number, number]}
          zoom={defaultZoom}
          style={{ width: "100%", height: "100%" }}
          maxBounds={bounds as [[number, number], [number, number]]}
          minZoom={11}
          maxZoom={18}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <MapClickHandler />
        </MapContainer>
      </MapWrapper>
    </div>
  );
};

export default Map;
