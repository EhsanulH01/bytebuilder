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
];

// --- DOM helpers ---
const $ = (sel, ctx = document) => ctx.querySelector(sel);

// --- State management ---
const state = {};

// --- Build the component selection grid ---
const buildComponentsGrid = () => {
  const grid = $("#componentsGrid");
  if (!grid) return;

  grid.innerHTML = "";

  ORDER.forEach((category) => {
    const card = document.createElement("div");
    card.className = "component-card";

    card.innerHTML = `
      <div class="component-header">
        <h3>${category}</h3>
        <span class="component-price" id="price-${category.replace(
          /\s+/g,
          "-"
        )}">$0</span>
      </div>
      <div class="component-selection">
        <button class="component-search-btn" onclick="openComponentSearch('${category}', this.parentElement.parentElement)">
          <span>Select ${category}</span>
          <span class="search-icon">🔍</span>
        </button>
        <div class="selected-component" style="display: none;"></div>
      </div>
    `;

    grid.appendChild(card);
  });
};

// --- Open component search modal ---
const openComponentSearch = (category, container) => {
  const modal = $("#partModal");
  const modalTitle = $("#modalTitle");
  const modalContent = $("#modalContent");

  modalTitle.textContent = `Select ${category}`;

  const componentsHtml = CATALOG[category]
    .map(
      (item) => `
    <div class="component-option" onclick="selectComponent('${category}', '${item.id}')">
      <img src="${item.image}" alt="${item.name}" class="component-image" />
      <div class="component-info">
        <h4>${item.name}</h4>
        <div class="component-price">$${item.price}</div>
        <div class="component-watts">${item.watts}W</div>
      </div>
      <button class="select-component-btn">Select</button>
    </div>
  `
    )
    .join("");

  modalContent.innerHTML = `
    <div class="components-list">
      ${componentsHtml}
    </div>
  `;

  // Store current container for selection
  modal.dataset.currentCategory = category;
  modal.dataset.currentContainer = container;

  modal.style.display = "block";
};

// --- Select component from search ---
const selectComponent = (category, itemId, element) => {
  const item = CATALOG[category].find((i) => i.id === itemId);
  if (!item) return;

  // Update state
  state[category] = item;

  // Find the container and update the UI
  const modal = $("#partModal");
  const container = modal.dataset.currentContainer;
  const searchBtn = container.querySelector(".component-search-btn");
  const selectedDiv = container.querySelector(".selected-component");
  const priceSpan = container.querySelector(".component-price");

  // Update button to show selected item
  searchBtn.className = "component-search-btn selected";
  searchBtn.innerHTML = `
    <span>✓ ${item.name}</span>
    <span class="search-icon">✓</span>
  `;

  // Show selected item details
  selectedDiv.innerHTML = `
    <div class="selected-item-display">
      <img src="${item.image}" alt="${item.name}" class="selected-img" />
      <div class="selected-info">
        <div class="selected-name">${item.name}</div>
        <div class="selected-specs">${item.watts}W • $${item.price}</div>
      </div>
    </div>
  `;
  selectedDiv.style.display = "block";

  // Update price
  priceSpan.textContent = `$${item.price}`;
  priceSpan.style.color = "var(--bg3)";

  // Close modal
  modal.style.display = "none";
};

// --- Show selected item with image ---
const showSelectedItem = (container, item, category) => {
  let selectedDisplay = container.querySelector(".selected-item");
  if (!selectedDisplay) {
    selectedDisplay = document.createElement("div");
    selectedDisplay.className = "selected-item";
    container.appendChild(selectedDisplay);
  }

  selectedDisplay.innerHTML = `
    <div class="selected-item-content">
      <img src="${item.image}" alt="${item.name}" class="selected-item-image" />
      <div class="selected-item-info">
        <div class="selected-item-name">${item.name}</div>
        <div class="selected-item-price">$${item.price}</div>
      </div>
      <button class="selected-item-details" onclick="showPartDetails('${category}', '${item.id}')">
        Details
      </button>
    </div>
  `;

  selectedDisplay.style.display = "block";
};

const hideSelectedItem = (container) => {
  const selectedDisplay = container.querySelector(".selected-item");
  if (selectedDisplay) {
    selectedDisplay.style.display = "none";
  }
};

// --- Show part details modal ---
const showPartDetails = (category, itemId) => {
  const item = CATALOG[category].find((i) => i.id === itemId);
  if (!item) return;

  const modal = $("#partModal");
  const modalTitle = $("#modalTitle");
  const modalContent = $("#modalContent");

  modalTitle.textContent = item.name;

  let specsHtml = "";
  if (item.specs) {
    specsHtml = Object.entries(item.specs)
      .map(
        ([key, value]) =>
          `<div class="spec-row"><span class="spec-key">${key}:</span> <span class="spec-value">${value}</span></div>`
      )
      .join("");
  }

  modalContent.innerHTML = `
    <div class="modal-item">
      <img src="${item.image}" alt="${item.name}" class="modal-image" />
      <div class="modal-info">
        <h4>${item.name}</h4>
        <div class="modal-price">$${item.price}</div>
        <div class="modal-specs">
          ${specsHtml}
        </div>
        <div class="modal-power">Power Consumption: ${item.watts}W</div>
      </div>
    </div>
  `;

  modal.style.display = "block";
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
      priceCell.textContent = `$${item.price}`;

      // Calculate performance score for CPU + GPU
      if (category === "CPU" || category === "GPU") {
        cpuGpuScore += item.score || 0;
      }
    } else {
      priceCell.textContent = "$0";
    }
  });

  // Update UI elements
  $("#totalPrice").textContent = `$${total}`;
  $("#wattBadge").textContent = `~ Wattage: ${totalWatts}W`;
  $("#perfScore").textContent = cpuGpuScore > 0 ? `${cpuGpuScore}/200` : "—";

  // Calculate PSU headroom
  const psu = state["Power Supply"];
  if (psu && totalWatts > 0) {
    const headroom = (((psu.watts - totalWatts) / psu.watts) * 100).toFixed(0);
    $("#psuHeadroom").textContent = `${headroom}%`;
  } else {
    $("#psuHeadroom").textContent = "—";
  }
};

// --- Reset and clear functions ---
const resetBuild = () => {
  Object.keys(state).forEach((key) => delete state[key]);

  // Reset all component cards
  const cards = document.querySelectorAll(".component-card");
  cards.forEach((card) => {
    const btn = card.querySelector(".component-search-btn");
    const selectedDiv = card.querySelector(".selected-component");
    const priceSpan = card.querySelector(".component-price");
    const category = card.querySelector("h3").textContent;

    btn.className = "component-search-btn";
    btn.innerHTML = `
      <span>Select ${category}</span>
      <span class="search-icon">🔍</span>
    `;
    selectedDiv.style.display = "none";
    priceSpan.textContent = "$0";
    priceSpan.style.color = "var(--muted)";
  });
};

// --- Export build ---
const exportBuild = () => {
  const buildList = ORDER.map((category) => {
    const item = state[category];
    return item
      ? `${category}: ${item.name} - $${item.price}`
      : `${category}: Not selected`;
  }).join("\n");

  const total = Object.values(state).reduce((sum, item) => sum + item.price, 0);
  const buildText = `My PC Build:\n\n${buildList}\n\nTotal: $${total}`;

  // Create a downloadable text file
  const blob = new Blob([buildText], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "my-pc-build.txt";
  a.click();
  URL.revokeObjectURL(url);
};

// --- Event listeners ---
document.addEventListener("DOMContentLoaded", () => {
  buildComponentsGrid();

  // Navigation
  $("#backToMainBtn").addEventListener("click", () => {
    window.location.href = "index.html";
  });

  // Build management
  $("#resetBtn").addEventListener("click", resetBuild);
  $("#clearBtn").addEventListener("click", resetBuild);
  $("#exportBtn").addEventListener("click", exportBuild);

  // Modal functionality
  $("#closeModal").addEventListener("click", () => {
    $("#partModal").style.display = "none";
  });

  // Close modal when clicking outside
  $("#partModal").addEventListener("click", (e) => {
    if (e.target.id === "partModal") {
      $("#partModal").style.display = "none";
    }
  });
});

// Make functions global so they can be called from onclick
window.showPartDetails = showPartDetails;
window.selectComponent = selectComponent;
window.openComponentSearch = openComponentSearch;
