<?php
session_start();

echo "<h2>Admin Controller Test</h2>";

// Set admin session
$_SESSION['user_id'] = 12;
$_SESSION['user_name'] = 'Admin User';
$_SESSION['user_email'] = 'admin12@gmail.com';
$_SESSION['is_admin'] = true;
$_SESSION['login_time'] = time();

echo "<p>Testing AdminController instantiation...</p>";

try {
    // Include configuration first
    require_once 'config/conf.php';
    echo "<p>✅ Configuration loaded</p>";
    
    // Include AdminController
    require_once 'app/Controllers/AdminController.php';
    echo "<p>✅ AdminController class loaded</p>";
    
    // Create AdminController instance
    $adminController = new AdminController();
    echo "<p>✅ AdminController instantiated successfully!</p>";
    
    // Test a method
    $stats = $adminController->getDashboardStats();
    echo "<p>✅ Dashboard stats retrieved:</p>";
    echo "<pre>" . print_r($stats, true) . "</pre>";
    
    echo "<p><a href='views/admin/dashboard.php'>Go to Admin Dashboard</a></p>";
    
} catch (Exception $e) {
    echo "<p style='color: red;'>❌ Error: " . $e->getMessage() . "</p>";
    echo "<p>Stack trace:</p>";
    echo "<pre>" . $e->getTraceAsString() . "</pre>";
}
?>
