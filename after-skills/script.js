// Filters the recipe cards by category tab, like flipping to a divider.
(function () {
  const tabs = document.querySelectorAll(".tab");
  const cards = document.querySelectorAll(".card-grid .index-card");
  const status = document.querySelector(".tab-status");

  function labelFor(filter) {
    if (filter === "all") return "all 10 cards";
    const tab = document.querySelector(`.tab[data-filter="${filter}"]`);
    return tab ? tab.textContent.trim() : filter;
  }

  function applyFilter(filter) {
    let visible = 0;
    cards.forEach(function (card) {
      const match = filter === "all" || card.dataset.category === filter;
      card.classList.toggle("is-hidden", !match);
      if (match) visible += 1;
    });

    tabs.forEach(function (tab) {
      const active = tab.dataset.filter === filter;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-pressed", String(active));
    });

    if (status) {
      status.textContent =
        visible + (visible === 1 ? " card filed under " : " cards filed under ") +
        labelFor(filter) + ".";
    }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      applyFilter(tab.dataset.filter);
    });
  });
})();
