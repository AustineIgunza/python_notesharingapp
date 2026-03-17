<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<h2>Form Submission Debug</h2>";
    echo "<h3>POST Data Received:</h3>";
    echo "<pre>";
    print_r($_POST);
    echo "</pre>";
    
    $admin_login = $_POST['admin_login'] ?? 'NOT SET';
    echo "<p><strong>admin_login value:</strong> '$admin_login'</p>";
    
    if ($admin_login == '1') {
        echo "<p style='color: green;'>✅ Admin mode detected! This should trigger admin login.</p>";
    } else {
        echo "<p style='color: red;'>❌ Admin mode NOT detected. Value is '$admin_login' instead of '1'.</p>";
        echo "<p><strong>Make sure you click the 'Admin Login' radio button!</strong></p>";
    }
} else {
?>
<!DOCTYPE html>
<html>
<head>
    <title>Form Submission Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .toggle { margin: 20px 0; }
        .radio-group { display: flex; gap: 10px; margin: 10px 0; }
        input[type="radio"] { margin-right: 5px; }
        input, button { padding: 8px; margin: 5px 0; }
        .debug { background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <h2>🔍 Signin Form Test</h2>
    
    <div class="debug">
        <h4>Instructions:</h4>
        <ol>
            <li><strong>Click "Admin Login" radio button</strong> (this is crucial!)</li>
            <li>Enter your credentials</li>
            <li>Click "Test Submit"</li>
            <li>Check if admin_login = '1' in the results</li>
        </ol>
    </div>
    
    <form method="POST" action="">
        <input type="hidden" name="signin" value="1">
        <input type="hidden" name="admin_login" id="admin_login_input" value="0">
        
        <div class="toggle">
            <h4>Login Mode:</h4>
            <div class="radio-group">
                <label>
                    <input type="radio" name="login_mode" id="mode_user" value="user" checked onchange="toggleLoginMode()">
                    👤 User Login
                </label>
                <label>
                    <input type="radio" name="login_mode" id="mode_admin" value="admin" onchange="toggleLoginMode()">
                    🔐 Admin Login ← <strong style="color: red;">CLICK THIS!</strong>
                </label>
            </div>
        </div>
        
        <div>
            <label>Email:</label><br>
            <input type="email" name="email" value="admin12@gmail.com" style="width: 300px;">
        </div>
        
        <div>
            <label>Password:</label><br>
            <input type="password" name="password" value="admin12" style="width: 300px;">
        </div>
        
        <div style="margin: 20px 0;">
            <button type="submit" id="submitBtn">
                <span id="submitText">👤 Sign In to Dashboard</span>
            </button>
        </div>
    </form>
    
    <div class="debug">
        <h4>Current Values (live update):</h4>
        <p>admin_login value: <span id="currentValue">0</span></p>
        <p>Submit button text: <span id="currentSubmitText">Sign In to Dashboard</span></p>
    </div>
    
    <script>
        function toggleLoginMode() {
            const isUser = document.getElementById('mode_user').checked;
            const adminInput = document.getElementById('admin_login_input');
            const submitText = document.getElementById('submitText');
            const currentValue = document.getElementById('currentValue');
            const currentSubmitText = document.getElementById('currentSubmitText');
            
            if (isUser) {
                // User Mode
                adminInput.value = '0';
                submitText.innerHTML = '👤 Sign In to Dashboard';
                currentValue.textContent = '0';
                currentSubmitText.textContent = 'Sign In to Dashboard';
            } else {
                // Admin Mode
                adminInput.value = '1';
                submitText.innerHTML = '🔐 Sign In as Admin';
                currentValue.textContent = '1';
                currentSubmitText.textContent = 'Sign In as Admin';
            }
        }
    </script>
</body>
</html>
<?php } ?>
