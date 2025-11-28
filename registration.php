<?php
$config = include 'config.php';

$mysqli = new mysqli(
    $config['db_host'],
    $config['db_user'],
    $config['db_pass'],
    $config['db_name'],
    $config['db_port']
);

if ($mysqli->connect_errno) {
    die("Database connection failed.");
}

$name     = $_POST['name'];
$email    = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_BCRYPT);
$contact  = $_POST['contact'];
$gender   = $_POST['gender'];

$stmt = $mysqli->prepare("
    INSERT INTO users (full_name, email, password, contact, gender)
    VALUES (?, ?, ?, ?, ?)
");

$stmt->bind_param("sssss", $name, $email, $password, $contact, $gender);

if ($stmt->execute()) {
    echo "<script>
            alert('Registered Successfully!');
            window.location.href = 'login.html';
          </script>";
} else {
    if ($stmt->errno == 1062) {
        echo "<script>
                alert('Email already exists! Try again.');
                window.location.href = 'registration.php';
              </script>";
    } else {
        echo "<script>
                alert('Registration failed due to an unexpected error.');
                window.location.href = 'registration.php';
              </script>";
    }
}

$stmt->close();
$mysqli->close();
?>
