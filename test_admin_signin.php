<?php
// Test admin signin functionality
session_start();

echo "<h2>Admin Signin Test</h2>";

// Simulate POST request
$_POST['signin'] = '1';
$_POST['admin_login'] = '1';
$_POST['email'] = 'admin12@gmail.com';
$_POST['password'] = 'admin12';
$_SERVER['REQUEST_METHOD'] = 'POST';

echo "<p>Testing admin login with:</p>";
echo "<ul>";
echo "<li>Email: admin12@gmail.com</li>";
echo "<li>Password: admin12</li>";
echo "<li>Admin login: 1</li>";
echo "</ul>";

// Include required files
require_once 'config/conf.php';
require_once 'config/Lang/en.php';
require_once 'app/Services/Global/Database.php';
require_once 'app/Services/Global/fncs.php';
require_once 'app/Services/Global/SendMail.php';
require_once 'app/Controllers/Proc/auth.php';

// instantiate helpers
$ObjFncs = new fncs();
$ObjSendMail = new SendMail();
$ObjAuth = new auth();
$db = new Database($conf);

echo "<h3>Testing Admin Direct Login Logic:</h3>";

$email = 'admin12@gmail.com';
$password = 'admin12';

if (!empty($email) && !empty($password)) {
    $user = null;
    
    // Try Database class first
    try {
        if (!$db->isStubMode()) {
            $stmt = $db->query("SELECT * FROM users WHERE email = ?", [$email]);
            $user = $stmt->fetch();
        }
        echo "<p>✅ Database class query successful</p>";
    } catch (Exception $e) {
        echo "<p>❌ Database class failed: " . $e->getMessage() . "</p>";
        $user = null;
    }
    
    // Fallback: Direct PDO connection if Database class fails
    if ($user === null) {
        try {
            $pdo = new PDO("mysql:host=127.0.0.1;dbname=notessharingapp;charset=utf8mb4", "root", "root", [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]);
            $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
            $stmt->execute([$email]);
            $user = $stmt->fetch();
            echo "<p>✅ Fallback PDO query successful</p>";
        } catch (Exception $e) {
            echo "<p>❌ Fallback PDO also failed: " . $e->getMessage() . "</p>";
        }
    }
    
    if ($user) {
        echo "<p>✅ User found: ID=" . $user['id'] . ", Email=" . $user['email'] . "</p>";
        
        if (password_verify($password, $user['password'])) {
            echo "<p>✅ Password verification successful</p>";
            
            // Check if user is admin using whitelist approach
            $admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];
            
            if (in_array($email, $admin_emails)) {
                echo "<p>✅ Admin user detected in whitelist</p>";
                
                // Test session setup
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['user_name'] = $user['full_name'];
                $_SESSION['user_email'] = $user['email'];
                $_SESSION['is_admin'] = true;
                $_SESSION['login_time'] = time();
                
                echo "<p>✅ Session variables set successfully</p>";
                echo "<p>🔗 Admin should redirect to: <strong>views/admin-dashboard.php</strong></p>";
                echo "<p><a href='views/admin-dashboard.php' target='_blank'>Test Admin Dashboard Access</a></p>";
            } else {
                echo "<p>❌ User not in admin whitelist</p>";
            }
        } else {
            echo "<p>❌ Password verification failed</p>";
        }
    } else {
        echo "<p>❌ User not found in database</p>";
    }
}

echo "<hr>";
echo "<h3>Current Session:</h3>";
echo "<pre>" . print_r($_SESSION, true) . "</pre>";

echo "<hr>";
echo "<p><a href='views/auth/signin.php'>Go to Main Signin Page</a></p>";
?>
