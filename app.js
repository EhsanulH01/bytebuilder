// --- Demo data (no external requests) ---

const CATALOG = {
  CPU: [
    {
      id: "r5-5600",
      name: "AMD Ryzen 5 5600",
      price: 129,
      watts: 65,
      score: 70,
    },
    {
      id: "r7-7800x3d",
      name: "AMD Ryzen 7 7800X3D",
      price: 369,
      watts: 120,
      score: 95,
    },
    {
      id: "i5-12400F",
      name: "Intel Core i5-12400F",
      price: 149,
      watts: 65,
      score: 72,
    },
    {
      id: "i7-13700K",
      name: "Intel Core i7-13700K",
      price: 389,
      watts: 125,
      score: 92,
    },
  ],
  GPU: [
    {
      id: "rtx-4060",
      name: "NVIDIA RTX 4060 8GB",
      price: 299,
      watts: 115,
      score: 70,
    },
    {
      id: "rtx-4070",
      name: "NVIDIA RTX 4070 12GB",
      price: 549,
      watts: 200,
      score: 86,
    },
    {
      id: "rx-7700xt",
      name: "AMD RX 7700 XT 12GB",
      price: 399,
      watts: 245,
      score: 82,
    },
    {
      id: "rx-7800xt",
      name: "AMD RX 7800 XT 16GB",
      price: 479,
      watts: 263,
      score: 88,
    },
  ],
  RAM: [
    { id: "16gb-3200", name: "16GB (2x8) DDR4-3200", price: 44, watts: 8 },
    { id: "32gb-3600", name: "32GB (2x16) DDR4-3600", price: 89, watts: 10 },
    { id: "32gb-ddr5", name: "32GB (2x16) DDR5-6000", price: 119, watts: 12 },
  ],
  Storage: [
    { id: "ssd-1tb", name: "1TB NVMe SSD (Gen3)", price: 59, watts: 5 },
    { id: "ssd-2tb", name: "2TB NVMe SSD (Gen4)", price: 129, watts: 6 },
    { id: "ssd-4tb", name: "4TB SATA SSD", price: 199, watts: 6 },
  ],
  Motherboard: [
    { id: "b550", name: "B550 ATX", price: 119, watts: 40 },
    { id: "b650", name: "B650 ATX", price: 169, watts: 45 },
    { id: "z690", name: "Z690 ATX", price: 219, watts: 50 },
  ],
  Case: [
    { id: "mesh-mid", name: "Mesh Mid-Tower", price: 79, watts: 0 },
    { id: "quiet-mid", name: "Quiet Mid-Tower", price: 129, watts: 0 },
    { id: "mini-itx", name: "Mini-ITX Small Form", price: 139, watts: 0 },
  ],
  "Power Supply": [
    { id: "psu-550", name: "550W 80+ Bronze", price: 59, watts: 550 },
    { id: "psu-650", name: "650W 80+ Gold", price: 89, watts: 650 },
    { id: "psu-750", name: "750W 80+ Gold", price: 109, watts: 750 },
    { id: "psu-850", name: "850W 80+ Gold", price: 129, watts: 850 },
  ],
  "Cooling System": [
    { id: "air-1", name: "120mm Air Cooler", price: 29, watts: 5 },
    { id: "air-2", name: "Dual-Tower Air Cooler", price: 69, watts: 7 },
    { id: "aio-240", name: "240mm AIO Liquid", price: 99, watts: 9 },
  ],
};

const ORDER = [
  "CPU",
  "GPU",
  "RAM",
  "Storage",
  "Motherboard",
  "Case",
  "Power Supply",
  "Cooling System",
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
  if (perfScoreEl) perfScoreEl.textContent = cpuGpuScore > 0 ? `${cpuGpuScore}/200` : "—";

  // Calculate PSU headroom
  const psu = state["Power Supply"];
  const psuHeadroomEl = $("#psuHeadroom");
  if (psuHeadroomEl) {
    if (psu && totalWatts > 0) {
      const headroom = (((psu.watts - totalWatts) / psu.watts) * 100).toFixed(0);
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

  const toTopBtn = $("#toTopBtn");
  if (toTopBtn) {
    toTopBtn.addEventListener("click", showIntro);
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
