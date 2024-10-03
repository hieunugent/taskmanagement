function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById('toggleIcon');
    sidebar.classList.toggle("active");   
        // Toggle visibility of both sidebar and content
    if (sidebar.style.display === "none") {
            sidebar.style.display = "block";
          
            toggleIcon.innerText = "chevron_left"; // Change button text
     } else {
            sidebar.style.display = "none";
            
            toggleIcon.innerText = "menu"; // Change button text
        }
  }