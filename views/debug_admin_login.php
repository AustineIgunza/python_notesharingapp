<?php
session_start();

echo "<h2>Testing Admin Login Process</h2>";

// Test the exact same process as signin.php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<h3>Processing Login...</h3>";
    
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $admin_login = $_POST['admin_login'] ?? '0';
    
    echo "Email: $email<br>";
    echo "Password: [" . strlen($password) . " chars]<br>";
    echo "Admin Login: $admin_login<br>";
    
    if ($admin_login == '1') {
        echo "<p style='color: blue;'>Admin login mode detected</p>";
        
        // Use direct PDO connection (like the fallback)
        try {
            $pdo = new PDO("mysql:host=127.0.0.1;dbname=notessharingapp;charset=utf8mb4", "root", "root", [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]);
            
            $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
            $stmt->execute([$email]);
            $user = $stmt->fetch();
            
            if ($user) {
                echo "<p style='color: green;'>✓ User found: " . $user['full_name'] . "</p>";
                
                if (password_verify($password, $user['password'])) {
                    echo "<p style='color: green;'>✓ Password verified</p>";
                    
                    if ($user['is_admin'] == 1) {
                        echo "<p style='color: green;'>✓ User is admin</p>";
                        
                        // Set session
                        $_SESSION['user_id'] = $user['id'];
                        $_SESSION['user_name'] = $user['full_name'];
                        $_SESSION['user_email'] = $user['email'];
                        $_SESSION['is_admin'] = true;
                        $_SESSION['login_time'] = time();
                        
                        echo "<p style='color: green;'>✓ Session variables set</p>";
                        echo "<p><strong>Session Data:</strong></p>";
                        echo "<pre>";
                        print_r($_SESSION);
                        echo "</pre>";
                        
                        // Instead of redirect, show what would happen
                        echo "<div style='background: #d4edda; padding: 15px; margin: 20px 0; border: 1px solid #c3e6cb;'>";
                        echo "<h4>✅ LOGIN SUCCESSFUL!</h4>";
                        echo "<p>In signin.php, this would redirect to: <code>../admin/dashboard.php</code></p>";
                        echo "<p>From views/auth/, this resolves to: <code>views/admin/dashboard.php</code></p>";
                        echo "<p><a href='admin/dashboard.php' style='color: blue;'>→ Click here to go to Admin Dashboard</a></p>";
                        echo "</div>";
                        
                    } else {
                        echo "<p style='color: red;'>✗ User is not admin (is_admin = " . $user['is_admin'] . ")</p>";
                    }
                } else {
                    echo "<p style='color: red;'>✗ Password verification failed</p>";
                }
            } else {
                echo "<p style='color: red;'>✗ User not found</p>";
            }
            
        } catch (Exception $e) {
            echo "<p style='color: red;'>Database error: " . $e->getMessage() . "</p>";
        }
        
    } else {
        echo "<p style='color: orange;'>Not admin login mode (admin_login = $admin_login)</p>";
    }
    
} else {
    // Show form
    ?>
    <form method="POST" action="">
        <div style="margin: 10px 0;">
            <label>Email:</label><br>
            <input type="email" name="email" value="admin12@gmail.com" style="width: 300px; padding: 5px;">
        </div>
        <div style="margin: 10px 0;">
            <label>Password:</label><br>
            <input type="password" name="password" value="admin12" style="width: 300px; padding: 5px;">
        </div>
        <input type="hidden" name="admin_login" value="1">
        <div style="margin: 10px 0;">
            <button type="submit" style="padding: 10px 20px; background: #007bff; color: white; border: none;">
                Test Admin Login
            </button>
        </div>
    </form>
    <?php
}

echo "<hr>";
echo "<p><a href='auth/signin.php'>← Back to Signin Page</a></p>";
?>
