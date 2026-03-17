<?php
// Simple admin login test
session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Direct Admin Login Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        form { border: 1px solid #ccc; padding: 20px; max-width: 400px; }
        input, button { margin: 5px 0; padding: 8px; width: 100%; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>Direct Admin Login Test</h2>
    
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['signin'])) {
        // Include required files from signin.php
        require_once 'config/conf.php';
        require_once 'config/Lang/en.php';
        require_once 'app/Services/Global/Database.php';
        require_once 'app/Services/Global/fncs.php';
        
        $ObjFncs = new fncs();
        $db = new Database($conf);
        
        // Force admin_login to 1 for this test
        $_POST['admin_login'] = '1';
        
        echo "<h3>Processing Admin Login...</h3>";
        echo "<p>POST data: " . print_r($_POST, true) . "</p>";
        
        if (isset($_POST['admin_login']) && $_POST['admin_login'] == '1') {
            echo "<p class='success'>✅ Admin login flag detected</p>";
            
            $email = $_POST['email'] ?? '';
            $password = $_POST['password'] ?? '';
            
            if (!empty($email) && !empty($password)) {
                $user = null;
                
                // Try Database class first
                try {
                    if (!$db->isStubMode()) {
                        $stmt = $db->query("SELECT * FROM users WHERE email = ?", [$email]);
                        $user = $stmt->fetch();
                    }
                    echo "<p class='success'>✅ Database class query successful</p>";
                } catch (Exception $e) {
                    echo "<p class='error'>❌ Database class failed: " . $e->getMessage() . "</p>";
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
                        echo "<p class='success'>✅ Fallback PDO query successful</p>";
                    } catch (Exception $e) {
                        echo "<p class='error'>❌ Fallback PDO also failed: " . $e->getMessage() . "</p>";
                    }
                }
                
                if ($user && password_verify($password, $user['password'])) {
                    echo "<p class='success'>✅ Password verification successful</p>";
                    
                    // Check if user is admin using whitelist approach
                    $admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];
                    
                    if (in_array($email, $admin_emails)) {
                        echo "<p class='success'>✅ User is in admin whitelist</p>";
                        
                        // Login directly without 2FA
                        $_SESSION['user_id'] = $user['id'];
                        $_SESSION['user_name'] = $user['full_name'];
                        $_SESSION['user_email'] = $user['email'];
                        $_SESSION['is_admin'] = true;
                        $_SESSION['login_time'] = time();
                        
                        echo "<p class='success'>✅ Admin session created successfully!</p>";
                        echo "<p><a href='views/admin/dashboard.php' target='_blank'>🚀 Go to Admin Dashboard</a></p>";
                        
                    } else {
                        echo "<p class='error'>❌ Admin access denied. You are not an administrator.</p>";
                    }
                } else {
                    echo "<p class='error'>❌ Invalid email or password.</p>";
                }
            } else {
                echo "<p class='error'>❌ Email or password is empty.</p>";
            }
        } else {
            echo "<p class='error'>❌ Admin login flag not detected</p>";
        }
    }
    ?>
    
    <form method="post">
        <h3>Test Admin Login</h3>
        <input type="hidden" name="signin" value="1">
        
        <label>Email:</label>
        <input type="email" name="email" value="admin12@gmail.com" required>
        
        <label>Password:</label>
        <input type="password" name="password" value="admin12" required>
        
        <button type="submit">Test Admin Login</button>
    </form>
    
    <hr>
    <h3>Current Session:</h3>
    <pre><?php print_r($_SESSION); ?></pre>
    
    <hr>
    <p><a href="views/auth/signin.php">Go to Main Signin Page</a></p>
</body>
</html>
