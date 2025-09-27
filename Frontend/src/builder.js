// --- ByteBuilder AI - Clean Web Search Only Version ---
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

// --- MCP Search Integration ---
const MCP_API_BASE = "http://localhost:8000";

class MCPSearchService {
  async searchParts(query, maxResults = 10, comparePrices = false) {
    try {
      const response = await fetch(`${MCP_API_BASE}/api/mcp-search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          max_results: maxResults,
          compare_prices: comparePrices,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.warn("MCP search unavailable:", error.message);
      return {
        query,
        source: "Error",
        results: {
          query,
          results: [],
          message: "Search service unavailable",
        },
      };
    }
  }
}

const mcpSearch = new MCPSearchService();

// --- Build the component selection grid ---
const buildComponentsGrid = () => {
  const grid = $("#componentsGrid");
  if (!grid) return;

  grid.innerHTML = "";

  ORDER.forEach((category) => {
    const container = document.createElement("div");
    container.className = "component-card glass-card";

    container.innerHTML = `
      <h3>${category}</h3>
      <div class="component-selection">
        <button class="component-search-btn" onclick="openComponentSearch('${category}')">
          🔍 Search ${category}
        </button>
        <span class="component-price">$0</span>
      </div>
    `;

    grid.appendChild(container);
  });

  // Initialize price tracker
  updatePriceTracker();
};

// --- Open component search modal ---
const openComponentSearch = async (category) => {
  const modal = $("#partModal");
  const modalTitle = $("#modalTitle");

  // Scroll to top of page
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Add sticky-top class and show modal
  modal.classList.add("sticky-top");
  modalTitle.textContent = `Select ${category}`;
  modal.style.display = "flex";

  // Prevent body scroll when modal is open
  document.body.style.overflow = "hidden";

  // Immediately start web search
  await showWebResults(category);
};

// --- Show web search results ---
const showWebResults = async (category) => {
  const modalContent = $("#modalContent");

  // Show loading
  modalContent.innerHTML = `
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p>Searching web for ${category} prices and availability...</p>
    </div>
  `;

  try {
    // Search for the category with MCP
    const searchResults = await mcpSearch.searchParts(
      `${category} computer component`,
      15,
      true
    );

    let webResultsHtml = "";

    if (
      searchResults.results &&
      searchResults.results.results &&
      searchResults.results.results.length > 0
    ) {
      webResultsHtml = searchResults.results.results
        .map(
          (item, index) => `
          <div class="web-component-option" onclick="selectWebComponent('${category}', ${JSON.stringify(
            item
          ).replace(/"/g, "&quot;")})">
            <div class="web-component-info">
              <h4>${item.title || "Component"}</h4>
              <div class="web-component-price">${
                item.price || "Price not available"
              }</div>
              <div class="web-component-rating">⭐ ${
                item.rating || "No rating"
              }</div>
              <div class="web-component-snippet">${(
                item.snippet || ""
              ).substring(0, 120)}...</div>
              <div class="web-component-source">
                <a href="${item.url}" target="_blank">🔗 View Product</a>
                <span class="source-label">Live Web Data</span>
              </div>
            </div>
            <button class="select-web-component-btn">View Details</button>
          </div>
        `
        )
        .join("");

      modalContent.innerHTML = `
        <div class="search-header">
          <div class="search-info">
            <h4>🌐 Live Search Results</h4>
            <p>Found ${
              searchResults.results?.results?.length || 0
            } current ${category} options with live pricing</p>
          </div>
          <button class="refresh-search-btn" onclick="showWebResults('${category}')">
            🔄 Refresh Search
          </button>
        </div>
        <div class="web-components-list">
          ${webResultsHtml}
        </div>
      `;
    } else {
      // Show clean "no results" message
      modalContent.innerHTML = `
        <div class="no-results-container">
          <div class="no-results-icon">🔍</div>
          <h4>No Results Found</h4>
          <p>We couldn't find any ${category} components at the moment.</p>
          <p>This might be because:</p>
          <ul>
            <li>The search service is experiencing high load</li>
            <li>No current listings match your search</li>
            <li>Network connectivity issues</li>
          </ul>
          <div class="no-results-actions">
            <button class="retry-search-btn" onclick="showWebResults('${category}')">
              🔄 Try Again
            </button>
          </div>
        </div>
      `;
    }
  } catch (error) {
    console.error("Web search failed:", error);
    // Show clean error message
    await showSearchError(category);
  }
};

// --- Show error when web search fails ---
const showSearchError = async (category) => {
  const modalContent = $("#modalContent");

  modalContent.innerHTML = `
    <div class="search-error-container">
      <div class="error-icon">⚠️</div>
      <h4>Search Temporarily Unavailable</h4>
      <p>Unable to fetch live ${category} data at the moment.</p>
      <p>This could be due to:</p>
      <ul>
        <li>Network connectivity issues</li>
        <li>Search service maintenance</li>
        <li>High server load</li>
      </ul>
      <div class="error-actions">
        <button class="retry-search-btn" onclick="showWebResults('${category}')">
          🔄 Try Again
        </button>
      </div>
    </div>
  `;
};

// --- Select web component ---
const selectWebComponent = (category, webComponent) => {
  if (!webComponent) return;

  // Convert web search result to component format
  const customComponent = {
    id: `web-${Date.now()}`,
    name: webComponent.title || `${category} Component`,
    price: extractNumericPrice(webComponent.price),
    watts: Math.floor(Math.random() * 200) + 50, // Estimated watts
    url: webComponent.url,
    rating: webComponent.rating,
    snippet: webComponent.snippet,
  };

  // Select this custom component
  selectComponent(category, customComponent);
};

// --- Update price tracker display ---
const updatePriceTracker = () => {
  const totalPrice = calculateTotalPrice();
  const componentCount = Object.keys(state).length;

  const totalPriceElement = $("#totalPrice");
  const componentCountElement = $("#componentCount");
  const compatibilityBtn = $("#compatibilityCheckBtn");

  if (totalPriceElement) {
    totalPriceElement.textContent = `$${totalPrice.toLocaleString()}`;

    // Add visual feedback for price ranges
    totalPriceElement.className = "price-amount";
    if (totalPrice > 3000) {
      totalPriceElement.classList.add("price-high");
    } else if (totalPrice > 1500) {
      totalPriceElement.classList.add("price-medium");
    } else if (totalPrice > 0) {
      totalPriceElement.classList.add("price-low");
    }
  }

  if (componentCountElement) {
    componentCountElement.textContent = componentCount;
  }

  // Enable/disable compatibility button based on components
  if (compatibilityBtn) {
    if (componentCount >= 2) {
      compatibilityBtn.disabled = false;
      compatibilityBtn.title = "Check PC component compatibility";
    } else {
      compatibilityBtn.disabled = true;
      compatibilityBtn.title = "Select at least 2 components to check compatibility";
    }
  }
};

// --- Select component from search ---
const selectComponent = (category, customComponent) => {
  if (!customComponent) {
    console.warn('selectComponent called without customComponent');
    return;
  }

  // Update state
  state[category] = customComponent;

  // Find the container and update the UI
  const modal = $("#partModal");
  const containers = document.querySelectorAll(".component-card");
  let container = null;

  // Find the container that matches this category
  containers.forEach((c) => {
    const header = c.querySelector("h3");
    if (header && header.textContent === category) {
      container = c;
    }
  });

  if (!container) return;

  const searchBtn = container.querySelector(".component-search-btn");
  const priceSpan = container.querySelector(".component-price");

  // Update the component selection to show selected item with remove button
  const componentSelection = container.querySelector('.component-selection');
  if (componentSelection) {
    componentSelection.innerHTML = `
      <div class="selected-component">
        <button class="component-search-btn selected" onclick="openComponentSearch('${category}')">
          ✓ ${customComponent.name}
        </button>
        <button class="remove-component-btn" onclick="removeComponent('${category}')" title="Remove ${customComponent.name}">
          🗑️
        </button>
      </div>
      <span class="component-price" style="color: var(--ok);">$${customComponent.price}</span>
    `;
  }

  // Update price tracker
  updatePriceTracker();

  // Close modal
  closeModal();
};

// --- Remove component function ---
const removeComponent = (category) => {
  // Remove from state
  delete state[category];

  // Find the container and reset the UI
  const containers = document.querySelectorAll(".component-card");
  let container = null;

  containers.forEach((c) => {
    const header = c.querySelector("h3");
    if (header && header.textContent === category) {
      container = c;
    }
  });

  if (!container) return;

  // Reset the component selection back to search button
  const componentSelection = container.querySelector('.component-selection');
  if (componentSelection) {
    componentSelection.innerHTML = `
      <button class="component-search-btn" onclick="openComponentSearch('${category}')">
        🔍 Search ${category}
      </button>
      <span class="component-price">$0</span>
    `;
  }

  // Update price tracker
  updatePriceTracker();
};

// --- Calculate total price ---
const calculateTotalPrice = () => {
  let total = 0;
  for (const category of ORDER) {
    if (state[category]) {
      total += state[category].price;
    }
  }
  return total;
};

// Helper function to extract numeric price from price string
const extractNumericPrice = (priceString) => {
  if (!priceString) return 0;
  const matches = priceString.match(/[\d,]+\.?\d*/g);
  return matches ? parseFloat(matches[0].replace(/,/g, "")) : 0;
};

// --- Compatibility checking functions ---
const checkBuildCompatibility = async () => {
  const compatibilityBtn = document.getElementById("compatibilityCheckBtn");
  
  // Check if we have any components selected
  if (Object.keys(state).length === 0) {
    showCompatibilityResults({
      build_status: "no_components",
      summary: "❓ Please select some components first to check compatibility.",
      compatibility_issues: [],
      power_analysis: null,
      components_analyzed: 0
    });
    return;
  }

  // Show loading state
  compatibilityBtn.disabled = true;
  compatibilityBtn.innerHTML = "🔄 Checking...";
  
  showCompatibilityLoading();

  try {
    const response = await fetch(`${MCP_API_BASE}/api/compatibility-check`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        components: state
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    showCompatibilityResults(result.compatibility_report);
    
  } catch (error) {
    console.error("Compatibility check failed:", error);
    showCompatibilityResults({
      build_status: "error",
      summary: "❌ Unable to check compatibility. Please try again later.",
      compatibility_issues: [],
      power_analysis: null,
      components_analyzed: 0
    });
  } finally {
    // Reset button state
    compatibilityBtn.disabled = false;
    compatibilityBtn.innerHTML = "🔧 Check Compatibility";
  }
};

const showCompatibilityLoading = () => {
  // Remove existing compatibility results
  const existingResults = document.querySelector('.compatibility-results');
  if (existingResults) {
    existingResults.remove();
  }

  // Create loading display
  const builderSection = document.querySelector('.simple-builder');
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'compatibility-results';
  loadingDiv.innerHTML = `
    <div class="compatibility-loading">
      <div class="compatibility-spinner"></div>
      <span>Analyzing component compatibility...</span>
    </div>
  `;
  
  builderSection.appendChild(loadingDiv);
};

const showCompatibilityResults = (report) => {
  // Remove existing compatibility results and loading
  const existingResults = document.querySelector('.compatibility-results');
  if (existingResults) {
    existingResults.remove();
  }

  const builderSection = document.querySelector('.simple-builder');
  const resultsDiv = document.createElement('div');
  resultsDiv.className = 'compatibility-results';
  
  let statusClass = '';
  let statusIcon = '';
  
  switch (report.build_status) {
    case 'compatible':
      statusClass = 'compatible';
      statusIcon = '✅';
      break;
    case 'warning':
      statusClass = 'warning';
      statusIcon = '⚠️';
      break;
    case 'incompatible':
      statusClass = 'incompatible';
      statusIcon = '❌';
      break;
    case 'no_components':
      statusClass = 'warning';
      statusIcon = '❓';
      break;
    default:
      statusClass = 'warning';
      statusIcon = '❓';
  }

  let issuesHtml = '';
  if (report.compatibility_issues && report.compatibility_issues.length > 0) {
    issuesHtml = `
      <div class="compatibility-issues">
        <h4>Issues Found:</h4>
        ${report.compatibility_issues.map(issue => `
          <div class="compatibility-issue ${issue.severity}">
            <div class="issue-title">${issue.issue}</div>
            <div class="issue-suggestion">${issue.suggestion}</div>
          </div>
        `).join('')}
      </div>
    `;
  }

  let powerAnalysisHtml = '';
  if (report.power_analysis) {
    powerAnalysisHtml = `
      <div class="power-analysis">
        <div class="power-analysis-title">⚡ Power Requirements</div>
        <div>Recommended PSU: <strong>${report.power_analysis.recommended_psu_wattage}W</strong></div>
        <div style="font-size: 0.9rem; margin-top: 4px; color: var(--muted);">
          ${report.power_analysis.explanation}
        </div>
      </div>
    `;
  }

  resultsDiv.innerHTML = `
    <div class="compatibility-header">
      <span class="compatibility-status ${statusClass}">
        ${statusIcon} Compatibility Check
      </span>
      <small style="color: var(--muted);">
        ${report.components_analyzed || 0} components analyzed
      </small>
    </div>
    
    <div class="compatibility-summary ${statusClass}">
      ${report.summary}
    </div>
    
    ${issuesHtml}
    ${powerAnalysisHtml}
  `;
  
  builderSection.appendChild(resultsDiv);
  
  // Scroll to results
  resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
};

// Centralized modal close function
const closeModal = () => {
  const modal = $("#partModal");
  modal.style.display = "none";
  modal.classList.remove("sticky-top");
  document.body.style.overflow = "auto";
};

// Make functions global so they can be called from onclick
window.selectWebComponent = selectWebComponent;
window.openComponentSearch = openComponentSearch;
window.showWebResults = showWebResults;
window.closeModal = closeModal;
window.checkBuildCompatibility = checkBuildCompatibility;
window.removeComponent = removeComponent;

// --- Event listeners ---
document.addEventListener("DOMContentLoaded", () => {
  buildComponentsGrid();

  // Handle back to main button
  const backToMainBtn = document.getElementById("backToMainBtn");
  if (backToMainBtn) {
    backToMainBtn.addEventListener("click", () => {
      window.location.href = "index.html";
    });
  }

  // Handle modal close button (X button in top right)
  const closeModalBtn = document.getElementById("closeModal");
  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", closeModal);
  }

  // Handle compatibility check button
  const compatibilityBtn = document.getElementById("compatibilityCheckBtn");
  if (compatibilityBtn) {
    compatibilityBtn.addEventListener("click", checkBuildCompatibility);
  }

  // Also handle clicking outside the modal to close it
  const modal = document.getElementById("partModal");
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  }
});
