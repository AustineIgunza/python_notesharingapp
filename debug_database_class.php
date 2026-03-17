<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h2>Database Class Debug</h2>";

try {
    require_once 'config/conf.php';
    
    echo "<h3>Configuration:</h3>";
    echo "<pre>";
    echo "DB Host: " . $conf['db_host'] . "\n";
    echo "DB Port: " . $conf['db_port'] . "\n";
    echo "DB Name: " . $conf['db_name'] . "\n";
    echo "DB User: " . $conf['db_user'] . "\n";
    echo "DB Pass Length: " . strlen($conf['db_pass']) . " chars\n";
    echo "</pre>";
    
    require_once 'app/Services/Global/Database.php';
    
    echo "<h3>Creating Database Instance:</h3>";
    $db = new Database($conf);
    echo "✓ Database object created successfully<br>";
    
    echo "Stub Mode: " . ($db->isStubMode() ? 'YES (No real DB connection)' : 'NO (Real connection)') . "<br>";
    
    if (!$db->isStubMode()) {
        echo "<h3>Testing Database Operations:</h3>";
        
        // Test 1: Simple query
        echo "<strong>Test 1: Simple query</strong><br>";
        $result = $db->query("SELECT 1 as test");
        $row = $result->fetch();
        echo "Result: " . json_encode($row) . "<br><br>";
        
        // Test 2: Check database name
        echo "<strong>Test 2: Current database</strong><br>";
        $result = $db->query("SELECT DATABASE() as current_db");
        $row = $result->fetch();
        echo "Current DB: " . $row['current_db'] . "<br><br>";
        
        // Test 3: Check users table exists
        echo "<strong>Test 3: Users table check</strong><br>";
        $result = $db->query("SHOW TABLES LIKE 'users'");
        $row = $result->fetch();
        if ($row) {
            echo "Users table exists<br>";
            
            // Test 4: Check is_admin column
            echo "<strong>Test 4: is_admin column check</strong><br>";
            $result = $db->query("SHOW COLUMNS FROM users LIKE 'is_admin'");
            $row = $result->fetch();
            if ($row) {
                echo "is_admin column exists<br>";
                
                // Test 5: Query admin users (the failing query)
                echo "<strong>Test 5: Admin users query (the one that fails)</strong><br>";
                $result = $db->fetchOne("SELECT is_admin FROM users WHERE id = ?", [1]);
                echo "Query result: " . json_encode($result) . "<br>";
                
            } else {
                echo "is_admin column missing!<br>";
            }
        } else {
            echo "Users table missing!<br>";
        }
    }
    
} catch (Exception $e) {
    echo "<div style='color: red; border: 1px solid red; padding: 10px; margin: 10px;'>";
    echo "<strong>Error:</strong> " . $e->getMessage() . "<br>";
    echo "<strong>File:</strong> " . $e->getFile() . "<br>";
    echo "<strong>Line:</strong> " . $e->getLine() . "<br>";
    echo "<strong>Trace:</strong><br>";
    echo "<pre style='white-space: pre-wrap;'>" . $e->getTraceAsString() . "</pre>";
    echo "</div>";
}

echo "<hr>";
echo "<p><a href='views/dashboard.php'>← Back to Dashboard</a></p>";
?>
