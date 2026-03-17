<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h2>Simple Database Test</h2>";

// Step 1: Load config exactly like the failing script
require_once 'config/conf.php';

echo "<h3>Config loaded:</h3>";
echo "DB Name: " . $conf['db_name'] . "<br>";

// Step 2: Create Database object exactly like the failing script  
require_once 'app/Services/Global/Database.php';

echo "<h3>Creating Database object...</h3>";
try {
    $db = new Database($conf);
    echo "✓ Database object created<br>";
    
    echo "Stub mode: " . ($db->isStubMode() ? 'YES' : 'NO') . "<br>";
    
    if (!$db->isStubMode()) {
        echo "<h3>Testing simple query...</h3>";
        $result = $db->fetchAll("SELECT 1 as test");
        echo "Query result: " . json_encode($result) . "<br>";
        
        echo "<h3>Testing users table...</h3>";
        $result = $db->fetchAll("SHOW TABLES LIKE 'users'");
        echo "Users table exists: " . (empty($result) ? 'NO' : 'YES') . "<br>";
        
        if (!empty($result)) {
            echo "<h3>Testing users query...</h3>";
            $users = $db->fetchAll("SELECT id, username, email FROM users LIMIT 2");
            echo "Sample users: " . json_encode($users) . "<br>";
        }
    }
    
} catch (Exception $e) {
    echo "<div style='color: red; border: 1px solid red; padding: 10px; margin: 10px;'>";
    echo "<strong>Error:</strong> " . $e->getMessage() . "<br>";
    echo "<strong>File:</strong> " . $e->getFile() . "<br>"; 
    echo "<strong>Line:</strong> " . $e->getLine() . "<br>";
    echo "<strong>Trace:</strong><br>";
    echo "<pre>" . $e->getTraceAsString() . "</pre>";
    echo "</div>";
}

echo "<hr>";
echo "<p><a href='test_admin_integration.php'>← Back to Admin Test</a></p>";
?>
