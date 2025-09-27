// --- Demo data (no external requests) ---

const ORDER = [
  "CPU",
  "GPU",
  "RAM",
  "Storage",
  "Motherboard",
  "Case",
  "Power Supply",
  "Cooling System",
  "Accessories",
];

// --- DOM helpers ---
const $ = (sel, ctx = document) => ctx.querySelector(sel);

// --- State management ---
const state = {};

// --- Page routing (two-page feel) ---
const showBuilder = () => {
  const intro = $("#intro");
  const partsShowcase = $("#parts-showcase");
  const builder = $("#builder");
  if (intro) intro.style.display = "none";
  if (partsShowcase) partsShowcase.style.display = "none";
  if (builder) builder.style.display = "block";
  window.scrollTo({ top: 0, behavior: "smooth" });
};
const showIntro = () => {
  const builder = $("#builder");
  const intro = $("#intro");
  const partsShowcase = $("#parts-showcase");
  if (builder) builder.style.display = "none";
  if (intro) intro.style.display = "block";
  if (partsShowcase) partsShowcase.style.display = "block";
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// --- Build the component selection table ---
const buildTable = () => {
  const tbody = $("#rows");
  if (!tbody) return;
  tbody.innerHTML = "";

  ORDER.forEach((category) => {
    const row = document.createElement("tr");

    // Component column
    const tdComponent = document.createElement("td");
    tdComponent.style.fontWeight = "600";
    tdComponent.textContent = category;

    // Selection column
    const tdSelection = document.createElement("td");
    const select = document.createElement("select");
    select.style.width = "100%";
    select.style.padding = "8px";
    select.style.background = "var(--card)";
    select.style.border = "1px solid var(--card-border)";
    select.style.borderRadius = "6px";
    select.style.color = "var(--text)";

    // Add default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = `Choose ${category}...`;
    select.appendChild(defaultOption);

    // Add component options
    CATALOG[category].forEach((item) => {
      const option = document.createElement("option");
      option.value = item.id;
      option.textContent = `${item.name} - $${item.price}`;
      select.appendChild(option);
    });

    select.addEventListener("change", (e) => {
      const selectedId = e.target.value;
      if (selectedId) {
        const selectedItem = CATALOG[category].find(
          (item) => item.id === selectedId
        );
        state[category] = selectedItem;
      } else {
        delete state[category];
      }
      updateSummary();
    });

    tdSelection.appendChild(select);

    // Price column
    const tdPrice = document.createElement("td");
    tdPrice.id = `price-${category.replace(/\s+/g, "-")}`;
    tdPrice.textContent = "$0";
    tdPrice.style.fontWeight = "600";

    row.appendChild(tdComponent);
    row.appendChild(tdSelection);
    row.appendChild(tdPrice);
    tbody.appendChild(row);
  });
};

// --- Update summary and calculations ---
const updateSummary = () => {
  let total = 0;
  let totalWatts = 0;
  let cpuGpuScore = 0;

  ORDER.forEach((category) => {
    const priceCell = $(`#price-${category.replace(/\s+/g, "-")}`);
    if (state[category]) {
      const item = state[category];
      total += item.price;
      totalWatts += item.watts || 0;
      if (priceCell) priceCell.textContent = `$${item.price}`;

      // Calculate performance score for CPU + GPU
      if (category === "CPU" || category === "GPU") {
        cpuGpuScore += item.score || 0;
      }
    } else {
      if (priceCell) priceCell.textContent = "$0";
    }
  });

  // Update UI elements
  const totalPriceEl = $("#totalPrice");
  if (totalPriceEl) totalPriceEl.textContent = `$${total}`;
  const wattBadgeEl = $("#wattBadge");
  if (wattBadgeEl) wattBadgeEl.textContent = `~ Wattage: ${totalWatts}W`;
  const perfScoreEl = $("#perfScore");
  if (perfScoreEl)
    perfScoreEl.textContent = cpuGpuScore > 0 ? `${cpuGpuScore}/200` : "—";

  // Calculate PSU headroom
  const psu = state["Power Supply"];
  const psuHeadroomEl = $("#psuHeadroom");
  if (psuHeadroomEl) {
    if (psu && totalWatts > 0) {
      const headroom = (((psu.watts - totalWatts) / psu.watts) * 100).toFixed(
        0
      );
      psuHeadroomEl.textContent = `${headroom}%`;
    } else {
      psuHeadroomEl.textContent = "—";
    }
  }
};

// --- Reset and clear functions ---
const resetBuild = () => {
  Object.keys(state).forEach((key) => delete state[key]);
  const selects = document.querySelectorAll("#rows select");
  selects.forEach((select) => (select.value = ""));
  updateSummary();
};

// Add reset button functionality
document.addEventListener("DOMContentLoaded", () => {
  $("#resetBtn")?.addEventListener("click", resetBuild);
  $("#clearBtn")?.addEventListener("click", resetBuild);
});

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
  // Build table if we're on a page that has it
  if ($("#rows")) {
    buildTable();
    updateSummary();
  }

  // Event listeners for navigation
  const startBtn = $("#startBtn");
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      window.location.href = "builder.html";
    });
  }

  const startBuildBtn = $("#startBuildBtn");
  if (startBuildBtn) {
    startBuildBtn.addEventListener("click", () => {
      window.location.href = "builder.html";
    });
  }

  const toBuilderTop = $("#toBuilderTop");
  if (toBuilderTop) {
    toBuilderTop.addEventListener("click", () => {
      window.location.href = "builder.html";
    });
  }

  const backBtn = $("#backBtn");
  if (backBtn) {
    backBtn.addEventListener("click", showIntro);
  }
  // Smooth scroll to parts showcase
  const learnBtn = $("#learnBtn");
  if (learnBtn) {
    learnBtn.addEventListener("click", () => {
      const partsShowcase = document.getElementById("parts-showcase");
      if (partsShowcase) {
        partsShowcase.scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  }
});
