const API = "http://localhost:5000";

export async function fetchArtists(page = 1, limit = 8, search = "") {
  const res = await fetch(`${API}/artists?page=${page}&limit=${limit}&search=${search}`);
  return res.json();
}

export async function fetchTracks(page = 1, limit = 8, search = "", minPop = 0, maxPop = 100) {
  const res = await fetch(`${API}/tracks?page=${page}&limit=${limit}&search=${search}&min_popularity=${minPop}&max_popularity=${maxPop}`);
  return res.json();
}
