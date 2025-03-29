import {
  MapContainer,
  TileLayer,
  useMapEvents,
  Marker,
  Popup,
} from "react-leaflet";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import { Marker as MarkerType } from "../types";

import "leaflet/dist/leaflet.css";
import styled from "styled-components";

// Fix for default marker icons in react-leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const MapWrapper = styled.div`
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
`;

interface MapProps {
  ClickHandler: (latlng: any) => void;
  LikeHandler: (marker: MarkerType) => void;
  DislikeHandler: (marker: MarkerType) => void;
  markers?: Array<MarkerType>;
}

const Map = (props: MapProps) => {
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
          {props.markers?.map((marker, index) => (
            <Marker key={index} position={marker.location}>
              <Popup>
                <h3>{marker.title}</h3>
                <p>{marker.body}</p>
                <div
                  style={{ display: "flex", gap: "10px", marginTop: "10px" }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      cursor: "pointer",
                      fontSize: "1.2em",
                      userSelect: "none",
                    }}
                    onClick={() => props.LikeHandler(marker)}
                  >
                    <span>👍 {marker.likes || 0}</span>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      cursor: "pointer",
                      fontSize: "1.2em",
                      userSelect: "none",
                    }}
                    onClick={() => props.DislikeHandler(marker)}
                  >
                    <span>👎 {marker.dislikes || 0}</span>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      fontSize: "1.2em",
                      userSelect: "none",
                    }}
                  >
                    <span>💬 {marker.replies?.length || 0}</span>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </MapWrapper>
    </div>
  );
};

export default Map;
