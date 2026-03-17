<?php
session_start();

echo "<h1>🎯 Admin Dashboard Test</h1>";

echo "<h3>Session Status:</h3>";
if (isset($_SESSION['user_id'])) {
    echo "<div style='background: #d4edda; padding: 15px; margin: 20px 0; border: 1px solid #c3e6cb; border-radius: 5px;'>";
    echo "<h4>✅ User Logged In</h4>";
    echo "<p><strong>User ID:</strong> " . $_SESSION['user_id'] . "</p>";
    echo "<p><strong>Name:</strong> " . $_SESSION['user_name'] . "</p>";
    echo "<p><strong>Email:</strong> " . $_SESSION['user_email'] . "</p>";
    echo "<p><strong>Is Admin:</strong> " . (isset($_SESSION['is_admin']) && $_SESSION['is_admin'] ? 'YES' : 'NO') . "</p>";
    echo "</div>";
    
    if (isset($_SESSION['is_admin']) && $_SESSION['is_admin']) {
        echo "<div style='background: #fff3cd; padding: 15px; margin: 20px 0; border: 1px solid #ffeaa7; border-radius: 5px;'>";
        echo "<h4>🔐 Admin Access Confirmed</h4>";
        echo "<p>You have successfully logged in as an administrator!</p>";
        echo "<p><a href='admin/dashboard.php' style='background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Go to Real Admin Dashboard</a></p>";
        echo "</div>";
    }
} else {
    echo "<div style='background: #f8d7da; padding: 15px; margin: 20px 0; border: 1px solid #f5c6cb; border-radius: 5px;'>";
    echo "<h4>❌ Not Logged In</h4>";
    echo "<p>No active session found.</p>";
    echo "<p><a href='admin_login.php' style='background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Go to Admin Login</a></p>";
    echo "</div>";
}

echo "<h3>Available Actions:</h3>";
echo "<p><a href='admin_login.php'>🔐 Admin Login</a></p>";
echo "<p><a href='admin/dashboard.php'>📊 Admin Dashboard</a></p>";
echo "<p><a href='dashboard.php'>👤 User Dashboard</a></p>";
echo "<p><a href='auth/signin.php'>🚪 Regular Sign In</a></p>";

if (isset($_SESSION['user_id'])) {
    echo "<p><a href='logout.php' style='color: red;'>🚪 Logout</a></p>";
}
?>
