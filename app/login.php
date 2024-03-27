<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/login.css">
    <title>4k Bluray</title>
</head>
<body>
    <header>
        <nav>
            <a class="logo">Bluray Paradise</a>
            <ul class="nav_menu">
                <li class="nav_link"><a href="index.php">Home</a></li>
                <li class="nav_link"><a href="#">Collection</a></li>
                <li class="nav_link"><a href="#">Wishlist</a></li>
                <li class="nav_link"><a href="#">Explore</a></li>
                <li class="nav_link active"><a href="#">Log In</a></li>
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

        <section class="login-page page">
            <div class="signup-wrap">
                <div class="signup-container">
                    <h1>Login</h1>

                    <form action="includes/process-login.php" method="post">
                        <input type="text" name="username" placeholder="Username">
                        <input type="password" name="pwd" placeholder="Password">
                        <button>Log In</button>
                    </form>

                </div>
            </div>
        </section>

        <section class="signup-page page">
            <div class="signup-wrap">
                <div class="signup-container">
                    <h1>Signup</h1>

                    <form action="includes/formhandler.php" method="post">
                        <input type="text" name="username" placeholder="Username">
                        <input type="password" name="pwd" placeholder="Password">
                        <input type="text" name="email" placeholder="Email">
                        <button>Sign in</button>
                    </form>

                </div>
            </div>
        </section>
    </div>

    <script src="js/animations.js"></script>
</body>
</html>