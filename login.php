<?php
session_start();

// Load secure config file
$config = include 'config.php';

// === Basic safety: only accept POST requests ===
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "Method Not Allowed";
    exit;
}

// === Get POST data safely ===
$email = isset($_POST['email']) ? trim($_POST['email']) : '';
$password = isset($_POST['password']) ? $_POST['password'] : '';

if ($email === '' || $password === '') {
    echo "Please provide both email and password.";
    exit;
}

// === DB connection ===
$mysqli = new mysqli(
    $config['db_host'],
    $config['db_user'],
    $config['db_pass'],
    $config['db_name'],
    $config['db_port']
);

if ($mysqli->connect_errno) {
    http_response_code(500);
    echo "Database connection failed.";
    exit;
}

// Query
$sql = "SELECT id, full_name, password FROM users WHERE email = ? LIMIT 1";
$stmt = $mysqli->prepare($sql);

$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows !== 1) {
    echo "❌ Email not found!";
    exit;
}

$stmt->bind_result($id, $name, $hashed_password);
$stmt->fetch();

// Verify password
if (password_verify($password, $hashed_password)) {
    $_SESSION["user_id"] = $id;
    $_SESSION["user_name"] = $name;

    echo "<script>
            alert('Login Successful!');
            window.location.href = '{$config['redirect_after_login']}';
          </script>";
    exit;
} else {
    echo "❌ Incorrect password!";
}

$stmt->close();
$mysqli->close();
?>
