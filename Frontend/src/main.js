// --- DOM helpers ---
const $ = (sel, ctx = document) => ctx.querySelector(sel);

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
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
