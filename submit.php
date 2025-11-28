<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// Load PHPMailer
require 'PHPMailer/src/Exception.php';
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';

// Load secure config
$config = include 'config.php';

// ===============================
// 1) DATABASE CONNECTION
// ===============================
$mysqli = new mysqli(
    $config["db_host"],
    $config["db_user"],
    $config["db_pass"],
    $config["db_name"],
    $config["db_port"]
);

if ($mysqli->connect_errno) {
    die("Database connection failed.");
}

// ===============================
// 2) GET FORM DATA SAFELY
// ===============================
$name            = trim($_POST['name']);
$email           = trim($_POST['email']);
$phone           = trim($_POST['phone']);
$preferred_date  = trim($_POST['preferred_date']);
$message         = trim($_POST['message']);

// ===============================
// 3) SAVE INTO DATABASE
// ===============================
$stmt = $mysqli->prepare("
    INSERT INTO appointments (name, email, phone, preferred_date, message)
    VALUES (?, ?, ?, ?, ?)
");

$stmt->bind_param("sssss", $name, $email, $phone, $preferred_date, $message);
$stmt->execute();
$stmt->close();

// ===============================
// 4) SEND EMAIL TO DOCTOR
// ===============================
$doctorEmail = $config["doctor_email"];

$mail = new PHPMailer(true);

try {
    // SMTP Settings
    $mail->isSMTP();
    $mail->Host       = $config["smtp_host"];
    $mail->SMTPAuth   = true;
    $mail->Username   = $config["smtp_user"];
    $mail->Password   = $config["smtp_pass"];
    $mail->SMTPSecure = $config["smtp_secure"];
    $mail->Port       = $config["smtp_port"];

    // Email headers
    $mail->setFrom($config["sender_email"], "Prakriti Consultation Website");
    $mail->addAddress($doctorEmail);
    $mail->addReplyTo($email, $name);

    // Email Content
    $mail->isHTML(true);
    $mail->Subject = "New Consultation Booking from $name";
    $mail->Body = "
        <h2>New Consultation Booking</h2>
        <p><strong>Name:</strong> $name</p>
        <p><strong>Email:</strong> $email</p>
        <p><strong>Phone:</strong> $phone</p>
        <p><strong>Preferred Date:</strong> $preferred_date</p>
        <p><strong>Health Concern:</strong></p>
        <p>$message</p>
    ";

    $mail->send();

    echo "<h2 style='color:green;'>✅ Consultation booked successfully!</h2>";
    echo "<p>Email sent to doctor.</p>";

} catch (Exception $e) {
    echo "<h2 style='color:red;'>❌ Email Failed</h2>";
    echo "<p>Error: {$mail->ErrorInfo}</p>";
}

$mysqli->close();
?>
