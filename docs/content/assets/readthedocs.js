// Use the hosted search addon when available; retain Material search locally.
let readthedocsSearchAvailable = false;
document.addEventListener("readthedocs-addons-data-ready", () => {
  readthedocsSearchAvailable = true;
});
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".md-search__input")?.addEventListener("focus", () => {
    if (readthedocsSearchAvailable) {
      document.dispatchEvent(new CustomEvent("readthedocs-search-show"));
    }
  });
});
