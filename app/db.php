<?php
    function connect_db() {
        $script_dir = dirname(__FILE__);

        $config_file = $script_dir . '/../config.json';
        $config_json = file_get_contents($config_file);
        $config = json_decode($config_json, true)['mysql'];

        $host = $config['host'];
        $name = $config['name'];
        $dsn = "mysql:host=$host;dbname=$name";
        $username = $config['user'];
        $password = $config['password'];

        try {
            $conn = new PDO($dsn, $username, $password);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            return $conn;
        } catch (PDOException $e) {
            die("Connection failed: " . $e->getMessage());
        }
    }

    function fetch($limit = 40, $offset = 0, $sale = null, $title = null, $status = null) {
        $conn = connect_db();
        
        $title_filter = "";
        if ($title != null) {
            $title_filter = "AND lower(title) like '%{$title}%'";
        }

        $status_filter = "";
        if ($status != null) {
            $status_filter = "AND lower(status) like '%{$status}%'";
        }

        $sale_filter = "";
        if ($sale != null) {
            $sale_filter = "AND sale != 0";
        }

        $query = "
            SELECT * FROM movies
            WHERE true
            $sale_filter
            $title_filter
            $status_filter
            ORDER BY sale DESC, current_price ASC, title
            LIMIT $limit
            OFFSET $offset;
        ";

        $result = $conn->query($query);

        $movies = $result->fetchAll(PDO::FETCH_ASSOC);

        $conn = null;

        return $movies;
    }