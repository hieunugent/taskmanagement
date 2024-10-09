 // Save scroll position before leaving or reloading the page
 window.addEventListener("beforeunload", function () {
    localStorage.setItem("scrollPosition", window.scrollY);
  });

  // Restore scroll position when the page loads
  window.addEventListener("load", function () {
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition) {
      window.scrollTo(0, scrollPosition);
      localStorage.removeItem("scrollPosition"); // Optional: Clear it after using
    }
  });