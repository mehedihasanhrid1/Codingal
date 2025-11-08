const menuBtn = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const menuIcon = document.getElementById('menu-icon');

menuBtn.addEventListener('click', () => {
  mobileMenu.classList.toggle('hidden');
  menuIcon.classList.toggle('fa-bars');
  menuIcon.classList.toggle('fa-x');
});

const slides = document.querySelectorAll('.slide');
const next = document.getElementById('next-slide');
const prev = document.getElementById('prev-slide');
let index = 0;

function showSlide(n) {
  slides.forEach((slide, i) => {
    slide.style.opacity = i === n ? '1' : '0';
    slide.style.zIndex = i === n ? '1' : '0';
  });
}

showSlide(index);

next.addEventListener('click', () => {
  index = (index + 1) % slides.length;
  showSlide(index);
});


prev.addEventListener('click', () => {
  index = (index - 1 + slides.length) % slides.length;
  showSlide(index);
});