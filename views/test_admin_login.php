<?php
session_start();

// Test admin login process
echo "<h2>Admin Login Test</h2>";

// Simulate the POST data
$_POST['admin_login'] = '1';
$_POST['email'] = 'admin12@gmail.com';
$_POST['password'] = 'admin12';
$_POST['signin'] = '1';

echo "<h3>Testing Admin Login Process:</h3>";
echo "Email: " . $_POST['email'] . "<br>";
echo "Password: " . $_POST['password'] . "<br>";
echo "Admin Login: " . $_POST['admin_login'] . "<br>";

try {
    require_once '../config/conf.php';
    require_once '../app/Services/Global/Database.php';
    
    $db = new Database($conf);
    echo "<p style='color: green;'>✓ Database connection successful</p>";
    
    if (!$db->isStubMode()) {
        echo "<h4>Verifying User Credentials:</h4>";
        
        $email = $_POST['email'];
        $password = $_POST['password'];
        
        // Test the exact query used in signin.php
        $stmt = $db->query("SELECT * FROM users WHERE email = ?", [$email]);
        $user = $stmt->fetch();
        
        if ($user) {
            echo "<p>✓ User found: " . $user['full_name'] . "</p>";
            echo "<p>User ID: " . $user['id'] . "</p>";
            echo "<p>Is Admin: " . ($user['is_admin'] ? 'YES' : 'NO') . "</p>";
            echo "<p>Is Verified: " . ($user['is_verified'] ? 'YES' : 'NO') . "</p>";
            echo "<p>2FA Enabled: " . ($user['is_2fa_enabled'] ? 'YES' : 'NO') . "</p>";
            
            if (password_verify($password, $user['password'])) {
                echo "<p style='color: green;'>✓ Password verification successful</p>";
                
                if ($user['is_admin'] == 1) {
                    echo "<p style='color: green;'>✓ User has admin privileges</p>";
                    echo "<p style='color: blue;'><strong>Login should succeed!</strong></p>";
                    
                    // Test session setting
                    $_SESSION['user_id'] = $user['id'];
                    $_SESSION['user_name'] = $user['full_name'];
                    $_SESSION['user_email'] = $user['email'];
                    $_SESSION['is_admin'] = true;
                    
                    echo "<p>Session set successfully. Ready for redirect to admin dashboard.</p>";
                    echo "<p><a href='admin/dashboard.php' style='color: blue;'>→ Test Admin Dashboard Access</a></p>";
                    
                } else {
                    echo "<p style='color: red;'>✗ User is not an admin</p>";
                }
            } else {
                echo "<p style='color: red;'>✗ Password verification failed</p>";
                echo "<p>Stored password hash: " . substr($user['password'], 0, 20) . "...</p>";
            }
        } else {
            echo "<p style='color: red;'>✗ User not found with email: $email</p>";
            
            // Check if user exists at all
            $all_users = $db->fetchAll("SELECT email, username FROM users WHERE email LIKE '%admin%'");
            echo "<p>Available admin emails:</p><ul>";
            foreach ($all_users as $u) {
                echo "<li>{$u['email']} ({$u['username']})</li>";
            }
            echo "</ul>";
        }
    } else {
        echo "<p style='color: orange;'>Database is in stub mode</p>";
    }
    
} catch (Exception $e) {
    echo "<p style='color: red;'>Error: " . $e->getMessage() . "</p>";
    echo "<p>File: " . $e->getFile() . ":" . $e->getLine() . "</p>";
}

echo "<hr>";
echo "<p><a href='auth/signin.php'>← Back to Signin Page</a></p>";
?>
