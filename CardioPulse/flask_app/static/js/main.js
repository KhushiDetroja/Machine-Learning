const toggleBtn = document.getElementById("themeToggle");

toggleBtn.addEventListener("click", () => {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");

    if (current === "dark") {
        html.setAttribute("data-theme", "light");
        toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        html.setAttribute("data-theme", "dark");
        toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }
});
