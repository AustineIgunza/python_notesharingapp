<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();

echo "<h2>Testing Admin Integration</h2>";

try {
    require_once 'config/conf.php';
    require_once 'app/Services/Global/Database.php';

    $db = new Database($conf);

    // Test 1: Check admin users exist
    echo "<h3>1. Admin Users in Database:</h3>";
    if ($db->isStubMode()) {
        echo "<p style='color: orange;'>⚠ Database is in stub mode - cannot query real data</p>";
        $admin_users = [];
    } else {
        $admin_users = $db->fetchAll("SELECT id, username, email, full_name, is_admin FROM users WHERE is_admin = 1");
    }
} catch (Exception $e) {
    echo "<div style='color: red; border: 1px solid red; padding: 10px; margin: 10px;'>";
    echo "<strong>Database Error:</strong> " . $e->getMessage() . "<br>";
    echo "<strong>File:</strong> " . $e->getFile() . "<br>"; 
    echo "<strong>Line:</strong> " . $e->getLine() . "<br>";
    echo "</div>";
    
    echo "<h3>Fallback: Direct Database Test</h3>";
    // Try direct database connection using config values
    try {
        $dsn = "mysql:host={$conf['db_host']};dbname={$conf['db_name']};charset=utf8mb4";
        echo "<p>Trying DSN: $dsn</p>";
        $options = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ];
        $pdo = new PDO($dsn, $conf['db_user'], $conf['db_pass'], $options);
        echo "<p style='color: green;'>✓ Direct PDO connection successful</p>";
        
        $stmt = $pdo->prepare("SELECT id, username, email, full_name, is_admin FROM users WHERE is_admin = 1");
        $stmt->execute();
        $admin_users = $stmt->fetchAll();
        
    } catch (Exception $e2) {
        echo "<p style='color: red;'>✗ Direct PDO also failed: " . $e2->getMessage() . "</p>";
        $admin_users = [];
    }
}
if (!empty($admin_users)) {
    echo "<table border='1'>";
    echo "<tr><th>ID</th><th>Username</th><th>Email</th><th>Full Name</th><th>Is Admin</th></tr>";
    foreach ($admin_users as $user) {
        echo "<tr>";
        echo "<td>{$user['id']}</td>";
        echo "<td>{$user['username']}</td>";
        echo "<td>{$user['email']}</td>";
        echo "<td>{$user['full_name']}</td>";
        echo "<td>{$user['is_admin']}</td>";
        echo "</tr>";
    }
    echo "</table>";
} else {
    echo "<p style='color: red;'>No admin users found!</p>";
}

// Test 2: Check admin controller exists
echo "<h3>2. Admin Controller Check:</h3>";
if (file_exists('app/Controllers/AdminController.php')) {
    echo "<p style='color: green;'>✓ AdminController.php exists</p>";
} else {
    echo "<p style='color: red;'>✗ AdminController.php missing</p>";
}

// Test 3: Check admin middleware exists
echo "<h3>3. Admin Middleware Check:</h3>";
if (file_exists('app/Middleware/AdminMiddleware.php')) {
    echo "<p style='color: green;'>✓ AdminMiddleware.php exists</p>";
} else {
    echo "<p style='color: red;'>✗ AdminMiddleware.php missing</p>";
}

// Test 4: Check admin views exist
echo "<h3>4. Admin Views Check:</h3>";
$admin_views = ['dashboard.php', 'users.php', 'notes.php', 'analytics.php'];
foreach ($admin_views as $view) {
    if (file_exists("views/admin/$view")) {
        echo "<p style='color: green;'>✓ views/admin/$view exists</p>";
    } else {
        echo "<p style='color: red;'>✗ views/admin/$view missing</p>";
    }
}

// Test 5: Check admin tables exist
echo "<h3>5. Admin Database Tables Check:</h3>";
$admin_tables = ['admin_activity_logs', 'user_suspensions', 'flagged_notes', 'system_statistics', 'admin_notifications', 'deleted_notes'];
foreach ($admin_tables as $table) {
    $result = $db->fetchOne("SHOW TABLES LIKE '$table'");
    if ($result) {
        echo "<p style='color: green;'>✓ Table '$table' exists</p>";
    } else {
        echo "<p style='color: red;'>✗ Table '$table' missing</p>";
    }
}

// Test 6: Session check
echo "<h3>6. Current Session:</h3>";
if (isset($_SESSION['user_id'])) {
    echo "<p>User ID: {$_SESSION['user_id']}</p>";
    echo "<p>User Name: {$_SESSION['user_name']}</p>";
    echo "<p>User Email: {$_SESSION['user_email']}</p>";
    
    // Check if current user is admin
    $user_admin_check = $db->fetchOne("SELECT is_admin FROM users WHERE id = ?", [$_SESSION['user_id']]);
    if ($user_admin_check && $user_admin_check['is_admin'] == 1) {
        echo "<p style='color: green;'>✓ Current user IS an admin</p>";
        echo "<p><a href='admin/dashboard.php' style='color: blue;'>→ Access Admin Panel</a></p>";
    } else {
        echo "<p style='color: orange;'>Current user is NOT an admin</p>";
    }
} else {
    echo "<p style='color: orange;'>No user logged in</p>";
    echo "<p><a href='auth/signin.php'>Sign in to test admin access</a></p>";
}

echo "<hr>";
echo "<p><a href='views/dashboard.php'>← Back to Dashboard</a></p>";
?>
