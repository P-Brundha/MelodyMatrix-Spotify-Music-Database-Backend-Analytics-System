import React, { useEffect, useState } from "react";
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
