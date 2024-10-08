function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById('toggleIcon');
    sidebar.classList.toggle("active");   
        // Toggle visibility of both sidebar and content
    if (sidebar.style.display === "none") {
            sidebar.style.display = "block";   
            toggleBtn.innerText = "chevron_left"; // Change button text
     } else {
            sidebar.style.display = "none";
            toggleBtn.innerText = "chevron_right"; // Change button text
        }
  }