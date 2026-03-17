<?php
echo "<h2>Database Connection Debug</h2>";

// Test 1: Check configuration
echo "<h3>1. Configuration Check:</h3>";
require_once 'config/conf.php';
echo "<pre>";
echo "DB Host: " . $conf['db_host'] . "\n";
echo "DB Port: " . $conf['db_port'] . "\n"; 
echo "DB Name: " . $conf['db_name'] . "\n";
echo "DB User: " . $conf['db_user'] . "\n";
echo "DB Pass: " . (empty($conf['db_pass']) ? '[EMPTY]' : '[SET - ' . strlen($conf['db_pass']) . ' chars]') . "\n";
echo "</pre>";

// Test 2: Direct PDO connection
echo "<h3>2. Direct PDO Connection Test:</h3>";
try {
    $dsn = "mysql:host={$conf['db_host']};port={$conf['db_port']};dbname={$conf['db_name']};charset=utf8mb4";
    echo "DSN: $dsn<br>";
    
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];
    
    $pdo = new PDO($dsn, $conf['db_user'], $conf['db_pass'], $options);
    echo "<p style='color: green;'>✓ Direct PDO connection successful!</p>";
    
    // Test query
    $stmt = $pdo->query("SELECT COUNT(*) as count FROM users");
    $result = $stmt->fetch();
    echo "<p>Users in database: {$result['count']}</p>";
    
} catch (Exception $e) {
    echo "<p style='color: red;'>✗ Direct PDO connection failed: " . $e->getMessage() . "</p>";
}

// Test 3: Database class connection
echo "<h3>3. Database Class Connection Test:</h3>";
try {
    require_once 'app/Services/Global/Database.php';
    $db = new Database($conf);
    echo "<p style='color: green;'>✓ Database class instantiated successfully!</p>";
    
    if ($db->isStubMode()) {
        echo "<p style='color: orange;'>⚠ Database is running in stub mode</p>";
    } else {
        echo "<p style='color: green;'>✓ Database is in normal mode</p>";
        
        // Test query through Database class
        $users = $db->fetchAll("SELECT COUNT(*) as count FROM users");
        echo "<p>Query test result: " . json_encode($users) . "</p>";
    }
    
} catch (Exception $e) {
    echo "<p style='color: red;'>✗ Database class failed: " . $e->getMessage() . "</p>";
}

echo "<hr>";
echo "<p><a href='test_admin_integration.php'>← Back to Admin Integration Test</a></p>";
?>
