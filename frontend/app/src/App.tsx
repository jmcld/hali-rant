import "./App.css";
import { Route, Routes } from "react-router";
import Home from "./pages/Home";
import About from "./pages/About";
import MapPage from "./pages/MapPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/map" element={<MapPage />} />
    </Routes>
  );
}

export default App;
