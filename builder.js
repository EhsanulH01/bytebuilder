// --- Demo data (no external requests) ---
const CATALOG = {
  CPU: [
    {
      id: "r5-5600",
      name: "AMD Ryzen 5 5600",
      price: 129,
      watts: 65,
      score: 70,
      image:
        "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=150&h=100&fit=crop&crop=center",
      specs: {
        cores: "6 cores / 12 threads",
        baseClock: "3.5 GHz",
        boostClock: "4.4 GHz",
        socket: "AM4",
      },
    },
    {
      id: "r7-7800x3d",
      name: "AMD Ryzen 7 7800X3D",
      price: 369,
      watts: 120,
      score: 95,
      image:
        "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=150&h=100&fit=crop&crop=center",
      specs: {
        cores: "8 cores / 16 threads",
        baseClock: "4.2 GHz",
        boostClock: "5.0 GHz",
        socket: "AM5",
      },
    },
    {
      id: "i5-12400F",
      name: "Intel Core i5-12400F",
      price: 149,
      watts: 65,
      score: 72,
      image:
        "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=150&h=100&fit=crop&crop=center",
      specs: {
        cores: "6 cores / 12 threads",
        baseClock: "2.5 GHz",
        boostClock: "4.4 GHz",
        socket: "LGA1700",
      },
    },
    {
      id: "i7-13700K",
      name: "Intel Core i7-13700K",
      price: 389,
      watts: 125,
      score: 92,
      image:
        "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=150&h=100&fit=crop&crop=center",
      specs: {
        cores: "16 cores / 24 threads",
        baseClock: "3.4 GHz",
        boostClock: "5.4 GHz",
        socket: "LGA1700",
      },
    },
  ],
  GPU: [
    {
      id: "rtx-4060",
      name: "NVIDIA RTX 4060 8GB",
      price: 299,
      watts: 115,
      score: 70,
      image:
        "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=150&h=100&fit=crop&crop=center",
      specs: {
        memory: "8GB GDDR6",
        baseClock: "1830 MHz",
        boostClock: "2460 MHz",
        interface: "PCIe 4.0",
      },
    },
    {
      id: "rtx-4070",
      name: "NVIDIA RTX 4070 12GB",
      price: 549,
      watts: 200,
      score: 86,
      image:
        "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=150&h=100&fit=crop&crop=center",
      specs: {
        memory: "12GB GDDR6X",
        baseClock: "1920 MHz",
        boostClock: "2475 MHz",
        interface: "PCIe 4.0",
      },
    },
    {
      id: "rx-7700xt",
      name: "AMD RX 7700 XT 12GB",
      price: 399,
      watts: 245,
      score: 82,
      image:
        "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=150&h=100&fit=crop&crop=center",
      specs: {
        memory: "12GB GDDR6",
        baseClock: "2171 MHz",
        boostClock: "2544 MHz",
        interface: "PCIe 4.0",
      },
    },
  ],
  RAM: [
    {
      id: "ddr4-16gb",
      name: "16GB DDR4-3200",
      price: 45,
      watts: 10,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1562976540-1502c2145186?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "16GB (2x8GB)",
        speed: "DDR4-3200",
        latency: "CL16",
        voltage: "1.35V",
      },
    },
    {
      id: "ddr4-32gb",
      name: "32GB DDR4-3600",
      price: 89,
      watts: 15,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1562976540-1502c2145186?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "32GB (2x16GB)",
        speed: "DDR4-3600",
        latency: "CL18",
        voltage: "1.35V",
      },
    },
    {
      id: "ddr5-32gb",
      name: "32GB DDR5-5600",
      price: 149,
      watts: 12,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1562976540-1502c2145186?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "32GB (2x16GB)",
        speed: "DDR5-5600",
        latency: "CL36",
        voltage: "1.25V",
      },
    },
  ],
  Storage: [
    {
      id: "ssd-500gb",
      name: "500GB NVMe SSD",
      price: 39,
      watts: 5,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1597872200969-2b65d56bd16c?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "500GB",
        interface: "NVMe PCIe 3.0",
        readSpeed: "3,400 MB/s",
        writeSpeed: "3,000 MB/s",
      },
    },
    {
      id: "ssd-1tb",
      name: "1TB NVMe SSD (Gen4)",
      price: 69,
      watts: 6,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1597872200969-2b65d56bd16c?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "1TB",
        interface: "NVMe PCIe 4.0",
        readSpeed: "7,000 MB/s",
        writeSpeed: "5,300 MB/s",
      },
    },
    {
      id: "ssd-2tb",
      name: "2TB NVMe SSD (Gen4)",
      price: 129,
      watts: 6,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1597872200969-2b65d56bd16c?w=150&h=100&fit=crop&crop=center",
      specs: {
        capacity: "2TB",
        interface: "NVMe PCIe 4.0",
        readSpeed: "7,000 MB/s",
        writeSpeed: "6,500 MB/s",
      },
    },
  ],
  Motherboard: [
    {
      id: "b550",
      name: "B550 ATX",
      price: 119,
      watts: 40,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1518276171653-104ff8db8b48?w=150&h=100&fit=crop&crop=center",
      specs: {
        socket: "AM4",
        formFactor: "ATX",
        memorySlots: "4x DIMM",
        maxMemory: "128GB",
      },
    },
    {
      id: "b650",
      name: "B650 ATX",
      price: 169,
      watts: 45,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1518276171653-104ff8db8b48?w=150&h=100&fit=crop&crop=center",
      specs: {
        socket: "AM5",
        formFactor: "ATX",
        memorySlots: "4x DIMM",
        maxMemory: "128GB",
      },
    },
    {
      id: "z690",
      name: "Z690 ATX",
      price: 219,
      watts: 50,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1518276171653-104ff8db8b48?w=150&h=100&fit=crop&crop=center",
      specs: {
        socket: "LGA1700",
        formFactor: "ATX",
        memorySlots: "4x DIMM",
        maxMemory: "128GB",
      },
    },
  ],
  Case: [
    {
      id: "mesh-mid",
      name: "Mesh Mid-Tower",
      price: 79,
      watts: 0,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=150&h=100&fit=crop&crop=center",
      specs: {
        formFactor: "Mid Tower",
        maxGpuLength: "330mm",
        fans: "3x 120mm included",
        sidePanel: "Tempered Glass",
      },
    },
    {
      id: "quiet-mid",
      name: "Quiet Mid-Tower",
      price: 129,
      watts: 0,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=150&h=100&fit=crop&crop=center",
      specs: {
        formFactor: "Mid Tower",
        maxGpuLength: "350mm",
        fans: "2x 140mm included",
        sidePanel: "Sound Dampened",
      },
    },
  ],
  "Power Supply": [
    {
      id: "psu-650",
      name: "650W 80+ Gold",
      price: 89,
      watts: 650,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1609205807107-e8ec2120f9de?w=150&h=100&fit=crop&crop=center",
      specs: {
        wattage: "650W",
        efficiency: "80+ Gold",
        modular: "Semi-Modular",
        warranty: "7 years",
      },
    },
    {
      id: "psu-750",
      name: "750W 80+ Gold",
      price: 109,
      watts: 750,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1609205807107-e8ec2120f9de?w=150&h=100&fit=crop&crop=center",
      specs: {
        wattage: "750W",
        efficiency: "80+ Gold",
        modular: "Fully Modular",
        warranty: "10 years",
      },
    },
  ],
  "Cooling System": [
    {
      id: "air-1",
      name: "120mm Air Cooler",
      price: 29,
      watts: 5,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=150&h=100&fit=crop&crop=center",
      specs: {
        type: "Air Cooler",
        fanSize: "120mm",
        height: "155mm",
        tdpRating: "150W",
      },
    },
    {
      id: "aio-240",
      name: "240mm AIO Liquid",
      price: 99,
      watts: 9,
      score: 0,
      image:
        "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=150&h=100&fit=crop&crop=center",
      specs: {
        type: "AIO Liquid",
        radiatorSize: "240mm",
        fanCount: "2x 120mm",
        tdpRating: "250W",
      },
    },
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
