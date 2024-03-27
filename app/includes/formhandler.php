<?php

if ($_SERVER["REQUEST_METHOD"] == "POST"){
    $username = $_POST["username"];
    $pwd = $_POST["pwd"];
    $email = $_POST["email"];
    
    try {
        require_once("db.php");
        $conn = connect_db();

        $query = "INSERT INTO users (username, pwd, email) VALUES (?,?,?);";

        $stmt = $conn->prepare($query);
        $stmt->execute([$username, $pwd, $email]);

        $conn = null;
        $stmt = null;

        header("Location: ../login.php");

        die();
    } catch (PDOException $e) {
        die("Query failed: ". $e->getMessage());
    }

} else {
    header("Location: ../login.php");
}