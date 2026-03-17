<?php
session_start();

require_once 'config/conf.php';
require_once 'app/Services/Global/Database.php';

$db = new Database($conf);

echo "<h2>Admin Login Test & Dashboard Preview</h2>";

// Simulate admin login
if (isset($_GET['login_as'])) {
    $user_id = intval($_GET['login_as']);
    $user = $db->fetchOne("SELECT * FROM users WHERE id = ? AND is_admin = 1", [$user_id]);
    
    if ($user) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['full_name'];
        $_SESSION['user_email'] = $user['email'];
        
        echo "<div style='background: #d4edda; color: #155724; padding: 10px; border: 1px solid #c3e6cb; margin: 10px 0;'>";
        echo "✓ Successfully logged in as {$user['full_name']} (Admin)";
        echo "</div>";
    }
}

// Check current session
if (isset($_SESSION['user_id'])) {
    echo "<h3>Current Session:</h3>";
    echo "<p><strong>User:</strong> {$_SESSION['user_name']}</p>";
    echo "<p><strong>Email:</strong> {$_SESSION['user_email']}</p>";
    
    // Check if current user is admin
    $user_admin_check = $db->fetchOne("SELECT is_admin FROM users WHERE id = ?", [$_SESSION['user_id']]);
    $is_admin = $user_admin_check && $user_admin_check['is_admin'] == 1;
    
    echo "<p><strong>Admin Status:</strong> " . ($is_admin ? '<span style="color: green;">YES</span>' : '<span style="color: red;">NO</span>') . "</p>";
    
    if ($is_admin) {
        echo "<div style='background: #fff3cd; color: #856404; padding: 10px; border: 1px solid #ffeaa7; margin: 10px 0;'>";
        echo "<strong>Admin Menu Should Be Visible:</strong><br>";
        echo "• In dropdown menu: Admin Panel link<br>";
        echo "• In sidebar: Admin Panel link<br>";
        echo "</div>";
        
        echo "<p><a href='views/dashboard.php' style='background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Go to Dashboard (Admin Menu Should Show)</a></p>";
        echo "<p><a href='views/admin/dashboard.php' style='background: #ffc107; color: black; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Access Admin Panel Directly</a></p>";
    }
    
    echo "<p><a href='?logout=1' style='color: red;'>Logout</a></p>";
} else {
    echo "<h3>Available Admin Users:</h3>";
    $admin_users = $db->fetchAll("SELECT id, username, email, full_name FROM users WHERE is_admin = 1");
    
    if (!empty($admin_users)) {
        echo "<ul>";
        foreach ($admin_users as $user) {
            echo "<li>";
            echo "<strong>{$user['full_name']}</strong> ({$user['username']}) - {$user['email']} ";
            echo "<a href='?login_as={$user['id']}' style='color: blue;'>[Login as this admin]</a>";
            echo "</li>";
        }
        echo "</ul>";
    } else {
        echo "<p style='color: red;'>No admin users found!</p>";
    }
}

// Handle logout
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: test_admin_dashboard.php');
    exit;
}

echo "<hr>";
echo "<p><a href='test_admin_integration.php'>← Back to Integration Test</a></p>";
?>
