<?php
session_start();

echo "<h2>Admin Credentials Debug</h2>";

// Test the exact credentials
$test_email = 'admin12@gmail.com';
$test_password = 'admin12';

echo "<h3>Testing Credentials:</h3>";
echo "Email: $test_email<br>";
echo "Password: $test_password<br>";

try {
    $pdo = new PDO("mysql:host=127.0.0.1;dbname=notessharingapp;charset=utf8mb4", "root", "root", [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    
    echo "<p style='color: green;'>✓ Database connection successful</p>";
    
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
    $stmt->execute([$test_email]);
    $user = $stmt->fetch();
    
    if ($user) {
        echo "<h3>User Found:</h3>";
        echo "ID: " . $user['id'] . "<br>";
        echo "Username: " . $user['username'] . "<br>";
        echo "Email: " . $user['email'] . "<br>";
        echo "Full Name: " . $user['full_name'] . "<br>";
        echo "Is Admin: " . ($user['is_admin'] ? 'YES' : 'NO') . "<br>";
        echo "Is Verified: " . ($user['is_verified'] ? 'YES' : 'NO') . "<br>";
        echo "2FA Enabled: " . ($user['is_2fa_enabled'] ? 'YES' : 'NO') . "<br>";
        echo "Password Hash: " . substr($user['password'], 0, 30) . "...<br>";
        
        echo "<h3>Password Verification Test:</h3>";
        $password_check = password_verify($test_password, $user['password']);
        echo "Password verification result: " . ($password_check ? 'SUCCESS ✓' : 'FAILED ✗') . "<br>";
        
        if (!$password_check) {
            echo "<h4>Fixing Password:</h4>";
            // Generate new password hash and update
            $new_hash = password_hash($test_password, PASSWORD_DEFAULT);
            echo "New password hash: " . substr($new_hash, 0, 30) . "...<br>";
            
            $update_stmt = $pdo->prepare("UPDATE users SET password = ? WHERE email = ?");
            $update_result = $update_stmt->execute([$new_hash, $test_email]);
            
            if ($update_result) {
                echo "<p style='color: green;'>✓ Password updated successfully!</p>";
                
                // Test again
                $verify_stmt = $pdo->prepare("SELECT password FROM users WHERE email = ?");
                $verify_stmt->execute([$test_email]);
                $new_user = $verify_stmt->fetch();
                
                $new_check = password_verify($test_password, $new_user['password']);
                echo "New password verification: " . ($new_check ? 'SUCCESS ✓' : 'FAILED ✗') . "<br>";
            } else {
                echo "<p style='color: red;'>✗ Failed to update password</p>";
            }
        }
        
        if ($user['is_admin'] != 1) {
            echo "<h4>Fixing Admin Status:</h4>";
            $admin_stmt = $pdo->prepare("UPDATE users SET is_admin = 1, is_verified = 1, is_2fa_enabled = 0 WHERE email = ?");
            $admin_result = $admin_stmt->execute([$test_email]);
            echo "Admin status updated: " . ($admin_result ? 'SUCCESS ✓' : 'FAILED ✗') . "<br>";
        }
        
    } else {
        echo "<h3 style='color: red;'>User NOT Found!</h3>";
        
        echo "<h4>Creating Admin User:</h4>";
        $password_hash = password_hash($test_password, PASSWORD_DEFAULT);
        
        $create_stmt = $pdo->prepare("
            INSERT INTO users (username, email, password, full_name, is_verified, is_2fa_enabled, is_admin, created_at, updated_at) 
            VALUES (?, ?, ?, ?, 1, 0, 1, NOW(), NOW())
        ");
        
        $create_result = $create_stmt->execute(['admin12', $test_email, $password_hash, 'Admin User']);
        
        if ($create_result) {
            echo "<p style='color: green;'>✓ Admin user created successfully!</p>";
        } else {
            echo "<p style='color: red;'>✗ Failed to create admin user</p>";
        }
    }
    
} catch (Exception $e) {
    echo "<p style='color: red;'>Database error: " . $e->getMessage() . "</p>";
}

echo "<hr>";
echo "<h3>Test Login Now:</h3>";
echo "<a href='admin_login.php' style='background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>→ Try Admin Login Again</a>";
?>
