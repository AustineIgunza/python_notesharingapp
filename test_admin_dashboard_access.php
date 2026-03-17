<?php
session_start();

// Test admin dashboard access
echo "<h2>Admin Dashboard Access Test</h2>";

// Set admin session for testing
$_SESSION['user_id'] = 12;
$_SESSION['user_name'] = 'Admin User';
$_SESSION['user_email'] = 'admin12@gmail.com';
$_SESSION['is_admin'] = true;
$_SESSION['login_time'] = time();

echo "<p>Session set for admin user.</p>";
echo "<p><a href='views/admin/dashboard.php'>Test Admin Dashboard Access</a></p>";

echo "<h3>Current Session:</h3>";
echo "<pre>" . print_r($_SESSION, true) . "</pre>";
?>
