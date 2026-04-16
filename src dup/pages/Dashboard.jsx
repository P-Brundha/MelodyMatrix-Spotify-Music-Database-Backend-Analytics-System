import React, { useEffect, useState } from "react";
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
