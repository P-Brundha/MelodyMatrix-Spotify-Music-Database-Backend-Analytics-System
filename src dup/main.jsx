import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Artists from "./pages/Artists";
import Tracks from "./pages/Tracks";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="p-4 bg-black text-white flex gap-6 text-lg font-semibold shadow-md">
          <Link to="/dashboard" className="hover:text-green-400">Dashboard</Link>
          <Link to="/artists" className="hover:text-green-400">Artists</Link>
          <Link to="/tracks" className="hover:text-green-400">Tracks</Link>
        </nav>
        <div className="p-6">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/artists" element={<Artists />} />
            <Route path="/tracks" element={<Tracks />} />
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
