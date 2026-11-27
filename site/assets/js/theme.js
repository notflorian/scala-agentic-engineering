(() => {
  const control = document.getElementById("theme");
  if (!control) return;

  const root = document.documentElement;
  control.value = root.dataset.theme || "system";
  document.getElementById("theme-control").hidden = false;
  control.addEventListener("change", () => {
    root.dataset.theme = control.value;
    try { localStorage.setItem("guide-theme", control.value); } catch {}
  });
})();
