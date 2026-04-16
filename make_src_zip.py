import os, zipfile

# Define structure
files = {
    "src/main.jsx": """import React from "react";
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
""",

    "src/api.js": """const API = "http://localhost:5000";

export async function fetchArtists(page = 1, limit = 8, search = "") {
  const res = await fetch(`${API}/artists?page=${page}&limit=${limit}&search=${search}`);
  return res.json();
}

export async function fetchTracks(page = 1, limit = 8, search = "", minPop = 0, maxPop = 100) {
  const res = await fetch(`${API}/tracks?page=${page}&limit=${limit}&search=${search}&min_popularity=${minPop}&max_popularity=${maxPop}`);
  return res.json();
}
""",

    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: system-ui, sans-serif;
}
""",

    "src/pages/Dashboard.jsx": """import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell
} from "recharts";
import axios from "axios";

const API = "http://localhost:5000";

export default function Dashboard() {
  const [topArtists, setTopArtists] = useState([]);
  const [topTracks, setTopTracks] = useState([]);
  const [tracksPerYear, setTracksPerYear] = useState([]);
  const [topGenres, setTopGenres] = useState([]);

  useEffect(() => {
    axios.get(`${API}/sql/top-artists`).then(res => setTopArtists(res.data));
    axios.get(`${API}/sql/top-tracks`).then(res => setTopTracks(res.data));
    axios.get(`${API}/sql/tracks-per-year`).then(res => setTracksPerYear(res.data));
    axios.get(`${API}/sql/top-genres`).then(res => setTopGenres(res.data));
  }, []);

  return (
    <div className="space-y-10">
      <h1 className="text-3xl font-bold">🎧 MelodyMatrix Dashboard</h1>

      <section>
        <h2 className="text-lg font-semibold mb-2">Top 10 Artists</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topArtists}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="popularity" fill="#6366f1" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">Top 10 Tracks</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topTracks}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" hide />
            <YAxis />
            <Tooltip />
            <Bar dataKey="popularity" fill="#22c55e" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">Popularity Trend by Year</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={tracksPerYear}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="release_year" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="avg_popularity" stroke="#f97316" />
          </LineChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-2">Top Genres</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={topGenres}
              dataKey="avg_popularity"
              nameKey="genre"
              outerRadius={120}
              label
            >
              {topGenres.map((_, index) => (
                <Cell
                  key={index}
                  fill={["#6366f1", "#22c55e", "#f97316", "#ec4899", "#0ea5e9"][index % 5]}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}
""",

    "src/pages/Artists.jsx": """import React, { useEffect, useState } from "react";
import { fetchArtists } from "../api";

export default function Artists() {
  const [artists, setArtists] = useState([]);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchArtists(page, 8, search).then((data) => {
      setArtists(data.artists);
      setTotal(data.total);
    });
  }, [page, search]);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">🎤 Artists</h2>

      <input
        type="text"
        placeholder="Search artist..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="border p-2 mb-6 w-full rounded"
      />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {artists.map((a) => (
          <div
            key={a.id}
            className="bg-white p-4 rounded-xl shadow hover:shadow-lg transition"
          >
            <div className="h-32 w-32 mx-auto bg-gradient-to-r from-purple-400 to-pink-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {a.name[0]}
            </div>
            <h3 className="mt-3 text-lg font-semibold text-center">{a.name}</h3>
            <p className="text-gray-500 text-sm text-center">{a.genres || "Unknown Genre"}</p>
            <p className="text-sm mt-1 text-center">Followers: {a.followers}</p>
            <p className="text-sm text-center">Popularity: ⭐ {a.popularity}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 flex gap-2 justify-center">
        <button disabled={page === 1} onClick={() => setPage(page - 1)} className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50">Prev</button>
        <span className="px-4 py-2">Page {page}</span>
        <button disabled={page * 8 >= total} onClick={() => setPage(page + 1)} className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50">Next</button>
      </div>
    </div>
  );
}
""",

    "src/pages/Tracks.jsx": """import React, { useEffect, useState } from "react";
import { fetchTracks } from "../api";

export default function Tracks() {
  const [tracks, setTracks] = useState([]);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [minPop, setMinPop] = useState(0);
  const [maxPop, setMaxPop] = useState(100);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchTracks(page, 8, search, minPop, maxPop).then((data) => {
      setTracks(data.tracks);
      setTotal(data.total);
    });
  }, [page, search, minPop, maxPop]);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">🎶 Tracks</h2>

      <div className="flex gap-4 mb-6">
        <input type="text" placeholder="Search track..." value={search} onChange={(e) => setSearch(e.target.value)} className="border p-2 rounded flex-1" />
        <input type="number" value={minPop} onChange={(e) => setMinPop(e.target.value)} className="border p-2 rounded w-20" />
        <span className="self-center">-</span>
        <input type="number" value={maxPop} onChange={(e) => setMaxPop(e.target.value)} className="border p-2 rounded w-20" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {tracks.map((t) => (
          <div key={t.id} className="bg-white p-4 rounded-xl shadow hover:shadow-lg transition">
            <div className="h-32 w-full bg-gradient-to-r from-green-400 to-blue-500 rounded flex items-center justify-center text-white text-2xl font-bold">
              🎵
            </div>
            <h3 className="mt-3 text-lg font-semibold">{t.name}</h3>
            <p className="text-gray-500 text-sm">{t.artists}</p>
            <p className="text-sm mt-1">Popularity: ⭐ {t.popularity}</p>
            <p className="text-sm">Released: {t.release_date}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 flex gap-2 justify-center">
        <button disabled={page === 1} onClick={() => setPage(page - 1)} className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50">Prev</button>
        <span className="px-4 py-2">Page {page}</span>
        <button disabled={page * 8 >= total} onClick={() => setPage(page + 1)} className="px-4 py-2 bg-gray-300 rounded disabled:opacity-50">Next</button>
      </div>
    </div>
  );
}
"""
}

# Create zip
with zipfile.ZipFile("src.zip", "w") as z:
    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        z.write(path)

print("✅ src.zip created successfully!")
