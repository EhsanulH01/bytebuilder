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
const MCP_API_BASE = 'http://localhost:8000';

class MCPSearchService {
  async searchParts(query, maxResults = 10, comparePrices = false) {
    try {
      const response = await fetch(`${MCP_API_BASE}/api/mcp-search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          max_results: maxResults,
          compare_prices: comparePrices
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.warn('MCP search unavailable:', error.message);
      return { 
        query, 
        source: 'Error',
        results: { 
          query, 
          results: [], 
          message: 'Search service unavailable' 
        } 
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
  
  modalTitle.textContent = `Select ${category}`;
  modal.style.display = "flex";
  
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
    const searchResults = await mcpSearch.searchParts(`${category} computer component`, 15, true);
    
    let webResultsHtml = '';
    
    if (searchResults.results && searchResults.results.results && searchResults.results.results.length > 0) {
      webResultsHtml = searchResults.results.results
        .map((item, index) => `
          <div class="web-component-option" onclick="selectWebComponent('${category}', ${JSON.stringify(item).replace(/"/g, '&quot;')})">
            <div class="web-component-info">
              <h4>${item.title || 'Component'}</h4>
              <div class="web-component-price">${item.price || 'Price not available'}</div>
              <div class="web-component-rating">⭐ ${item.rating || 'No rating'}</div>
              <div class="web-component-snippet">${(item.snippet || '').substring(0, 120)}...</div>
              <div class="web-component-source">
                <a href="${item.url}" target="_blank">🔗 View Product</a>
                <span class="source-label">Live Web Data</span>
              </div>
            </div>
            <button class="select-web-component-btn">View Details</button>
          </div>
        `)
        .join("");
        
      modalContent.innerHTML = `
        <div class="search-header">
          <div class="search-info">
            <h4>🌐 Live Search Results</h4>
            <p>Found ${searchResults.results?.results?.length || 0} current ${category} options with live pricing</p>
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
    console.error('Web search failed:', error);
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
    snippet: webComponent.snippet
  };
  
  // Select this custom component
  selectComponent(category, customComponent.id, customComponent);
};

// --- Update price tracker display ---
const updatePriceTracker = () => {
  const totalPrice = calculateTotalPrice();
  const componentCount = Object.keys(state).length;
  
  const totalPriceElement = $("#totalPrice");
  const componentCountElement = $("#componentCount");
  
  if (totalPriceElement) {
    totalPriceElement.textContent = `$${totalPrice.toLocaleString()}`;
    
    // Add visual feedback for price ranges
    totalPriceElement.className = 'price-amount';
    if (totalPrice > 3000) {
      totalPriceElement.classList.add('price-high');
    } else if (totalPrice > 1500) {
      totalPriceElement.classList.add('price-medium');
    } else if (totalPrice > 0) {
      totalPriceElement.classList.add('price-low');
    }
  }
  
  if (componentCountElement) {
    componentCountElement.textContent = componentCount;
  }
};

// --- Select component from search ---
const selectComponent = (category, itemId, customComponent = null) => {
  let item;
  
  if (customComponent) {
    // Use custom component from web search
    item = customComponent;
  } else {
    // This should only be called with customComponent now
    console.warn('selectComponent called without customComponent - this should not happen in web-only mode');
    return;
  }
  
  if (!item) return;

  // Update state
  state[category] = item;

  // Find the container and update the UI
  const modal = $("#partModal");
  const containers = document.querySelectorAll('.component-card');
  let container = null;
  
  // Find the container that matches this category
  containers.forEach(c => {
    const header = c.querySelector('h3');
    if (header && header.textContent === category) {
      container = c;
    }
  });
  
  if (!container) return;
  
  const searchBtn = container.querySelector(".component-search-btn");
  const priceSpan = container.querySelector(".component-price");

  // Hide search button, show selected item
  if (searchBtn) {
    searchBtn.textContent = `✓ ${item.name}`;
    searchBtn.classList.add('selected');
  }

  // Update price
  if (priceSpan) {
    priceSpan.textContent = `$${item.price}`;
    priceSpan.style.color = "var(--ok)";
  }

  // Update price tracker
  updatePriceTracker();

  // Close modal
  modal.style.display = "none";
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

// --- Calculate total power consumption ---
const calculateTotalWatts = () => {
  let totalWatts = 0;
  for (const category of ORDER) {
    if (state[category]) {
      totalWatts += state[category].watts || 0;
    }
  }
  return totalWatts;
};

// --- Export build as text file ---
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

// Helper function to extract numeric price from price string
const extractNumericPrice = (priceString) => {
  if (!priceString) return 0;
  const matches = priceString.match(/[\d,]+\.?\d*/g);
  return matches ? parseFloat(matches[0].replace(/,/g, '')) : 0;
};

// Make functions global so they can be called from onclick
window.selectComponent = selectComponent;
window.selectWebComponent = selectWebComponent;
window.openComponentSearch = openComponentSearch;
window.showWebResults = showWebResults;
window.showSearchError = showSearchError;
window.closeModal = () => $("#partModal").style.display = "none";

// --- Event listeners ---
document.addEventListener("DOMContentLoaded", () => {
  buildComponentsGrid();
  
  // Handle back to main button
  const backToMainBtn = document.getElementById('backToMainBtn');
  if (backToMainBtn) {
    backToMainBtn.addEventListener('click', () => {
      window.location.href = 'index.html';
    });
  }
  
  // Handle modal close button (X button in top right)
  const closeModalBtn = document.getElementById('closeModal');
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      document.getElementById('partModal').style.display = 'none';
    });
  }
  
  // Also handle clicking outside the modal to close it
  const modal = document.getElementById('partModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
      }
    });
  }
});