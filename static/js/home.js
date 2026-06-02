// MOBILE MENU TOGGLE

const menuBtn = document.getElementById("mobile-menu");
const mobileNavMenu = document.getElementById("mobile-nav");

menuBtn.addEventListener("click", () => {

    mobileNavMenu.classList.toggle("show-menu");

});

