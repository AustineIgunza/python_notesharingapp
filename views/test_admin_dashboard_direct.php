<?php
session_start();

// Set admin session for testing
$_SESSION['user_id'] = 7;
$_SESSION['user_name'] = 'Admin User'; 
$_SESSION['user_email'] = 'admin12@gmail.com';
$_SESSION['is_admin'] = true;

echo "<h2>Admin Dashboard Direct Test</h2>";

echo "<h3>Session Data:</h3>";
echo "<pre>";
print_r($_SESSION);
echo "</pre>";

echo "<h3>Testing Admin Dashboard Access:</h3>";
echo "<p><a href='admin/dashboard.php' style='background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Go to Admin Dashboard</a></p>";

echo "<p><strong>If the link works, the AdminMiddleware is fixed!</strong></p>";
echo "<p>If it redirects to regular dashboard, there's still an issue with the middleware.</p>";

echo "<hr>";
echo "<p><a href='admin_login.php'>← Back to Admin Login</a></p>";
?>
