// Selección de elementos del DOM
const barramenu = document.getElementById("barramenu");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

// Maneja el clic en el menú principal
menu.addEventListener("click", () => {
    barraLateral.classList.toggle("max-barra-lateral");
    
    // Cambia iconos del menú según el estado de la barra lateral
    menu.children[0].style.display = barraLateral.classList.contains("max-barra-lateral") ? "none" : "block";
    menu.children[1].style.display = barraLateral.classList.contains("max-barra-lateral") ? "block" : "none";
    
    // Ajusta la barra lateral si el ancho de la ventana es pequeño
    if (window.innerWidth <= 320) {
        barraLateral.classList.add("mini-barra-lateral");
        main.classList.add("min-main");
        spans.forEach(span => span.classList.add("oculto"));
    }
});

// Maneja el clic en el switch de modo oscuro
palanca.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    circulo.classList.toggle("prendido");
});

// Maneja el clic en la barra de menú
barramenu.addEventListener("click", () => {
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach(span => span.classList.toggle("oculto"));
});
