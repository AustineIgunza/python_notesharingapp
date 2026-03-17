<?php
echo "<h2>Database Name Debug</h2>";

// Test both database names
$databases_to_test = ['notessharingapp', 'notessharingapp'];

foreach ($databases_to_test as $db_name) {
    echo "<h3>Testing database: '$db_name'</h3>";
    
    try {
        $pdo = new PDO("mysql:host=127.0.0.1;dbname=$db_name;charset=utf8mb4", "root", "root", [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
        
        echo "<p style='color: green;'>✓ Connection successful to '$db_name'</p>";
        
        // Check if users table exists
        $stmt = $pdo->query("SHOW TABLES LIKE 'users'");
        if ($stmt->fetch()) {
            echo "<p>✓ Users table exists</p>";
            
            // Check table structure
            $stmt = $pdo->query("DESCRIBE users");
            $columns = $stmt->fetchAll(PDO::FETCH_COLUMN);
            
            if (in_array('is_admin', $columns)) {
                echo "<p style='color: green;'>✓ is_admin column exists</p>";
                
                // Try to query admin users
                $stmt = $pdo->prepare("SELECT id, username, email, is_admin FROM users WHERE is_admin = 1");
                $stmt->execute();
                $admin_users = $stmt->fetchAll();
                
                echo "<p>Admin users found: " . count($admin_users) . "</p>";
                if (!empty($admin_users)) {
                    foreach ($admin_users as $user) {
                        echo "<p>- {$user['username']} ({$user['email']})</p>";
                    }
                }
            } else {
                echo "<p style='color: red;'>✗ is_admin column missing</p>";
                echo "<p>Available columns: " . implode(', ', $columns) . "</p>";
            }
        } else {
            echo "<p style='color: red;'>✗ Users table does not exist</p>";
        }
        
    } catch (Exception $e) {
        echo "<p style='color: red;'>✗ Connection failed: " . $e->getMessage() . "</p>";
    }
    
    echo "<hr>";
}
?>
