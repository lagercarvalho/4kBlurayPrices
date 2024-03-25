let currentIndex = {
    "top_sale": 0,
    "sale_steelbooks": 0,
    "bookable_movies": 0,
};
var itemsPerSlide = 0;

function renderMovies(className) {
    var movie_list = document.getElementsByClassName(className);

    for (let i = 0; i < movie_list.length; i++) {
        movie_list[i].style.display = "none";
    }

    var endIndex = Math.min(currentIndex[className] + itemsPerSlide, movie_list.length);
    for (var i = currentIndex[className]; i < endIndex; i++) {
        movie_list[i].style.display = "block";
    }
}

function renderAll(){
    for (let key in currentIndex){
        renderMovies(key);
    }
}

function prevSlide(className) {
    if (currentIndex[className] > 0) {
        currentIndex[className] -= itemsPerSlide;
        renderMovies(className);
    }
}

function nextSlide(className) {
    var movie_list = document.getElementsByClassName(className);
    if (currentIndex[className] + itemsPerSlide < movie_list.length) {
        currentIndex[className] += itemsPerSlide;
        renderMovies(className);
    }
}

function checkWidth() {
    var pageWidth = document.documentElement.clientWidth;
    var elements = Math.floor(pageWidth / 260);

    if (elements != itemsPerSlide){
        itemsPerSlide = elements;
        renderAll();
    }
}

// Initial rendering
checkWidth();

window.addEventListener('resize', function(event) {
    checkWidth()
});

