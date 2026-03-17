<?php
session_start();

// Process login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // Direct database connection
    try {
        $pdo = new PDO("mysql:host=127.0.0.1;dbname=notessharingapp;charset=utf8mb4", "root", "root", [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]);
        
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        // Check if user exists and password is correct
        if ($user && password_verify($password, $user['password'])) {
            // Check if this is an admin email (simple whitelist approach)
            $admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];
            
            if (in_array($email, $admin_emails)) {
                // Set session
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['user_name'] = $user['full_name'];
                $_SESSION['user_email'] = $user['email'];
                $_SESSION['is_admin'] = true;
                $_SESSION['login_time'] = time();
                
                // Show success and redirect
                echo "<div style='background: #d4edda; color: #155724; padding: 15px; margin: 20px 0; border: 1px solid #c3e6cb; border-radius: 5px;'>";
                echo "<h4>🎉 Admin Login Successful!</h4>";
                echo "<p>Welcome, " . $user['full_name'] . "!</p>";
                echo "<p>Redirecting to admin dashboard...</p>";
                echo "<p><a href='admin/dashboard.php'>Click here if not redirected automatically</a></p>";
                echo "</div>";
                
                // JavaScript redirect as backup
                echo "<script>
                    console.log('Admin login successful, redirecting...');
                    setTimeout(function() {
                        window.location.href = 'admin/dashboard.php';
                    }, 2000);
                </script>";
                
                // Try header redirect too
                header('Location: admin/dashboard.php');
                exit();
            } else {
                $error = "You are not an administrator";
            }
        } else {
            $error = "Invalid credentials";
        }
        
    } catch (Exception $e) {
        $error = "Connection error: " . $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Direct</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        .admin-badge {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 1.5rem;
            font-weight: bold;
        }
        .btn-admin {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px;
            font-weight: bold;
        }
        .btn-admin:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="text-center">
            <div class="admin-badge">
                <i class="bi bi-shield-lock me-2"></i>Admin Access
            </div>
            <h3 class="mb-4">Admin Login</h3>
        </div>

        <?php if (isset($error)): ?>
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle me-2"></i><?php echo $error; ?>
            </div>
        <?php endif; ?>

        <form method="POST" action="">
            <div class="mb-3">
                <label for="email" class="form-label">
                    <i class="bi bi-envelope me-2"></i>Admin Email
                </label>
                <input type="email" class="form-control" id="email" name="email" 
                       value="admin12@gmail.com" required>
            </div>
            
            <div class="mb-4">
                <label for="password" class="form-label">
                    <i class="bi bi-lock me-2"></i>Password
                </label>
                <input type="password" class="form-control" id="password" name="password" 
                       value="admin12" required>
            </div>
            
            <button type="submit" class="btn btn-admin btn-primary w-100 mb-3">
                <i class="bi bi-box-arrow-in-right me-2"></i>Login as Admin
            </button>
        </form>

        <div class="text-center">
            <small class="text-muted">
                <i class="bi bi-info-circle me-1"></i>
                Direct admin access - No 2FA required
            </small>
        </div>

        <hr class="my-4">
        
        <div class="text-center">
            <a href="auth/signin.php" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-arrow-left me-2"></i>Back to Regular Login
            </a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
