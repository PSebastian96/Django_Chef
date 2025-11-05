document.addEventListener("DOMContentLoaded", function() {
const currentPath = window.location.pathname; // e.g., /recipes/
const links = document.querySelectorAll(".offcanvas .nav-link");

    links.forEach(link => {
      const linkPath = new URL(link.href).pathname;
      if (linkPath === currentPath) {
        link.classList.add("current");
      }
    });
  });

