<?php
    require_once("includes/db.php");
    $script_dir = dirname(__DIR__);
    $sale_rows = fetch(sale: "true");
    $sale_steelbooks = fetch(sale: "true", title:"steelbook");
    $bookable_movies = fetch(status:"bookable");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/movies.css">
    <title>4k Bluray</title>
</head>
<body>
    <header>
        <nav>
            <a class="logo">Bluray Paradise</a>
            <ul class="nav_menu">
                <li class="nav_link active"><a href="index.php">Home</a></li>
                <li class="nav_link"><a href="#">Collection</a></li>
                <li class="nav_link"><a href="#">Wishlist</a></li>
                <li class="nav_link"><a href="#">Explore</a></li>
                <li class="nav_link"><a href="login.php">Log In</a></li>
            </ul>
            <button class="hamburger-button" aria-expanded="false">
                <svg fill="var(--button-color)" class="hamburger" viewbox="0 0 100 100" width="100%">
                    <rect class="line top" 
                    width="80" height="10"
                    x="10" y="25" rx="5"></rect>
                    <rect class="line middle" 
                    width="80" height="10"
                    x="10" y="45" rx="5"></rect>
                    <rect class="line bottom" 
                    width="80" height="10"
                    x="10" y="65" rx="5"></rect>
                </svg>
            </button>
        </nav>   
    </header>

    <div class="container">
        <section class="sec-container">
            <h1 class="title">Top Sales</h1>
            <div class="content_container">
                <?php foreach ($sale_rows as $movie): ?>
                    <div class="movie_container top_sale fade">
                        <div class="poster">
                            <a href="<?php echo htmlspecialchars($movie['list_src']); ?>" target="_blank"><img src="<?php echo htmlspecialchars($movie['img_src']); ?>" alt="<?php echo htmlspecialchars($movie['title']); ?>"></a>
                        </div>
                        <div class="movie_info">
                            <div class="title_container">
                                <p><?php echo htmlspecialchars($movie['title']); ?></p>
                            </div>
                            <div class="price_container">
                                <span><?php echo htmlspecialchars($movie['current_price']); ?>kr</span>
                                <?php if ($movie['sale'] != 0): ?>
                                    <span class="old"><?php echo htmlspecialchars($movie['previous_price']); ?>kr</span>
                                    <span class="sale"><?php echo htmlspecialchars(sprintf("%.0f", $movie['sale'] * 100)); ?>%</span>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
                <a class="slider-arrow left" onclick="prevSlide('top_sale')">&#10094;</a>
                <a class="slider-arrow right" onclick="nextSlide('top_sale')">&#10095;</a>
            </div>
        </section>

        <section class="sec-container">
            <h1 class="title">Steelbook sales</h1>
            <div class="content_container">
                <?php foreach ($sale_steelbooks as $movie): ?>
                    <div class="movie_container sale_steelbooks fade">
                        <div class="poster">
                            <a href="<?php echo htmlspecialchars($movie['list_src']); ?>" target="_blank"><img src="<?php echo htmlspecialchars($movie['img_src']); ?>" alt="<?php echo htmlspecialchars($movie['title']); ?>"></a>
                        </div>
                        <div class="movie_info">
                            <div class="title_container">
                                <p><?php echo htmlspecialchars($movie['title']); ?></p>
                            </div>
                            <div class="price_container">
                                <span><?php echo htmlspecialchars($movie['current_price']); ?>kr</span>
                                <?php if ($movie['sale'] != 0): ?>
                                    <span class="old"><?php echo htmlspecialchars($movie['previous_price']); ?>kr</span>
                                    <span class="sale"><?php echo htmlspecialchars(sprintf("%.0f", $movie['sale'] * 100)); ?>%</span>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
                <a class="slider-arrow left" onclick="prevSlide('sale_steelbooks')">&#10094;</a>
                <a class="slider-arrow right" onclick="nextSlide('sale_steelbooks')">&#10095;</a>
            </div>
        </section>

        <section class="sec-container">
            <h1 class="title">Coming soon</h1>
            <div class="content_container">
                <?php foreach ($bookable_movies as $movie): ?>
                    <div class="movie_container bookable_movies fade">
                        <div class="poster">
                            <a href="<?php echo htmlspecialchars($movie['list_src']); ?>" target="_blank"><img src="<?php echo htmlspecialchars($movie['img_src']); ?>" alt="<?php echo htmlspecialchars($movie['title']); ?>"></a>
                        </div>
                        <div class="movie_info">
                            <div class="title_container">
                                <p><?php echo htmlspecialchars($movie['title']); ?></p>
                            </div>
                            <div class="price_container">
                                <span><?php echo htmlspecialchars($movie['current_price']); ?>kr</span>
                                <?php if ($movie['sale'] != 0): ?>
                                    <span class="old"><?php echo htmlspecialchars($movie['previous_price']); ?>kr</span>
                                    <span class="sale"><?php echo htmlspecialchars(sprintf("%.0f", $movie['sale'] * 100)); ?>%</span>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
                <a class="slider-arrow left" onclick="prevSlide('bookable_movies')">&#10094;</a>
                <a class="slider-arrow right" onclick="nextSlide('bookable_movies')">&#10095;</a>
            </div>
        </section>
    </div>

    <script src="js/animations.js"></script>
    <script src="js/slides.js"></script>
</body>
</html>