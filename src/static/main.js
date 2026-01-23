let page = 0;
let loading = false;

async function load() {
  if (loading) return;
  loading = true;

  const res = await fetch(`/api/media?page=${page}`);
  const data = await res.json();

  if (!data.length) return;

  const grid = document.getElementById("grid");

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

  page++;
  loading = false;
}

window.addEventListener("scroll", () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300) {
    load();
  }
});

load();
