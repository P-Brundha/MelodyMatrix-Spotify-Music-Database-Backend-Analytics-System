import React, { useEffect, useState } from "react";
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
