let page = 0;         // current page index to request from the API
let loading = false;  // gate to prevent concurrent/duplicate loads

async function load() {
  if (loading) return;   // bail out if a load is already in progress
  loading = true;        // set gate to block other loads

  // fetch one page from the backend API
  const res = await fetch(`/api/media?page=${page}`);
  const data = await res.json();

  if (!data.length) return;  // no more items: stop (note: loading stays true here)

  const grid = document.getElementById("grid");

  // append each item to the grid: create <video> for videos, <img> for images
  data.forEach(m => {
    let el;
    if (m.type === "video") {
      el = document.createElement("video");
      el.src = m.url;
      el.controls = true;
    } else {
      el = document.createElement("img");
      el.src = m.url;
    }
    grid.appendChild(el);
  });

  page++;            // advance to next page for subsequent loads
  loading = false;   // release gate so next load can run
}

window.addEventListener("scroll", () => {
  // trigger load when near the bottom (300px). Use >= to avoid off-by-one issues.
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300) {
    load();  // call loader
  }
});

load();  // initial load for page 0
