<?php
session_start();

// Simulate the exact conditions from dashboard.php
$_SESSION['user_id'] = 5; // Use testuser admin account

require_once '../config/conf.php';
require_once '../app/Services/Global/Database.php';

echo "<h2>Dashboard Database Query Test</h2>";

echo "<h3>Session Data:</h3>";
echo "User ID: " . $_SESSION['user_id'] . "<br>";

try {
    echo "<h3>Creating Database Object:</h3>";
    $db = new Database($conf);
    echo "✓ Database object created<br>";
    echo "Stub mode: " . ($db->isStubMode() ? 'YES' : 'NO') . "<br>";
    
    if (!$db->isStubMode()) {
        echo "<h3>Testing the exact query that fails in dashboard.php:</h3>";
        
        $user_id = $_SESSION['user_id'];
        echo "Querying for user ID: $user_id<br>";
        
        // This is the exact query from dashboard.php line 45
        $admin_check = $db->fetchOne("SELECT is_admin FROM users WHERE id = ?", [$user_id]);
        
        echo "Query result: " . json_encode($admin_check) . "<br>";
        
        if ($admin_check) {
            $is_admin = $admin_check['is_admin'] == 1;
            echo "Is admin: " . ($is_admin ? 'YES' : 'NO') . "<br>";
        } else {
            echo "No user found with ID $user_id<br>";
        }
    }
    
} catch (Exception $e) {
    echo "<div style='color: red; border: 1px solid red; padding: 10px;'>";
    echo "<strong>Error:</strong> " . $e->getMessage() . "<br>";
    echo "<strong>File:</strong> " . $e->getFile() . "<br>";
    echo "<strong>Line:</strong> " . $e->getLine() . "<br>";
    echo "</div>";
}

echo "<hr>";
echo "<p><a href='dashboard.php'>← Try Dashboard Again</a></p>";
?>
