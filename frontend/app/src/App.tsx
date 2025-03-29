import "./App.css";
import { Route, Routes } from "react-router";
import Home from "./pages/Home";
import Map from "./pages/Map";
import About from "./pages/About";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/map" element={<Map />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}

export default App;
