<?php
session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login Debug</title>
</head>
<body>
    <h2>Admin Login Debug Test</h2>
    
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        echo "<h3>POST Data Received:</h3>";
        echo "<pre>" . print_r($_POST, true) . "</pre>";
        
        if (isset($_POST['signin']) && isset($_POST['admin_login']) && $_POST['admin_login'] == '1') {
            echo "<p><strong>✅ Admin login detected!</strong></p>";
            
            $email = $_POST['email'] ?? '';
            $password = $_POST['password'] ?? '';
            
            echo "<p>Testing credentials: $email / $password</p>";
            
            if ($email === 'admin12@gmail.com' && $password === 'admin12') {
                echo "<p>✅ Credentials match! Setting up session...</p>";
                
                $_SESSION['user_id'] = 12;
                $_SESSION['user_name'] = 'Admin User';
                $_SESSION['user_email'] = $email;
                $_SESSION['is_admin'] = true;
                $_SESSION['login_time'] = time();
                
                echo "<p>✅ Session set. <a href='../admin-dashboard.php'>Go to Admin Dashboard</a></p>";
            } else {
                echo "<p>❌ Credentials don't match</p>";
            }
        } else {
            echo "<p>❌ Admin login not detected or admin_login != 1</p>";
            echo "<p>admin_login value: " . ($_POST['admin_login'] ?? 'NOT SET') . "</p>";
        }
    }
    ?>
    
    <form method="post">
        <input type="hidden" name="signin" value="1">
        <input type="hidden" name="admin_login" id="admin_login_input" value="0">
        
        <div>
            <label>
                <input type="radio" name="login_mode" value="user" checked onchange="toggleMode()"> User Login
            </label>
        </div>
        <div>
            <label>
                <input type="radio" name="login_mode" value="admin" onchange="toggleMode()"> Admin Login
            </label>
        </div>
        
        <div>
            <label>Email:</label>
            <input type="email" name="email" value="admin12@gmail.com" required>
        </div>
        
        <div>
            <label>Password:</label>
            <input type="password" name="password" value="admin12" required>
        </div>
        
        <button type="submit">Sign In</button>
    </form>
    
    <script>
    function toggleMode() {
        const adminRadio = document.querySelector('input[name="login_mode"][value="admin"]');
        const adminInput = document.getElementById('admin_login_input');
        
        if (adminRadio.checked) {
            adminInput.value = '1';
            console.log('Admin mode activated, admin_login set to 1');
        } else {
            adminInput.value = '0';
            console.log('User mode activated, admin_login set to 0');
        }
    }
    </script>
</body>
</html>
