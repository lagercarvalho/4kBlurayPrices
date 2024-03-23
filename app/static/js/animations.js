const button = document.querySelector('.hamburger-button');
const menu = document.querySelector('.nav_menu');

button.addEventListener('click', () => {
    const isOpened = button.getAttribute('aria-expanded');
    if (isOpened === 'false'){
        button.setAttribute('aria-expanded', 'true');
    } else {
        button.setAttribute('aria-expanded', 'false');
        
    }
    menu.classList.toggle("active");
})

document.querySelectorAll(".nav_link").forEach(link => link.addEventListener("click", () => {
    button.setAttribute('aria-expanded', 'false');
    menu.classList.remove("active");
}))