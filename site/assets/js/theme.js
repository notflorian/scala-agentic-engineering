(() => {
  const dark = document.getElementById("dark-theme");
  function apply(choice) {
    dark.media = choice === "dark" ? "all" : choice === "light" ? "not all" : "(prefers-color-scheme: dark)";
  }
  let choice = "system";
  try { choice = localStorage.getItem("guide-theme") || choice; } catch {}
  apply(choice);
  document.addEventListener("DOMContentLoaded", () => {
    const control = document.getElementById("theme");
    control.value = choice;
    control.addEventListener("change", () => {
      apply(control.value);
      try { localStorage.setItem("guide-theme", control.value); } catch {}
    });
  });
})();
