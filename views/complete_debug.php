<?php
session_start();

echo "<h2>Complete Admin Login Debug</h2>";

$email = 'admin12@gmail.com';
$password = 'admin12';

echo "<h3>Step 1: Database Connection</h3>";
try {
    $pdo = new PDO("mysql:host=127.0.0.1;dbname=notessharingapp;charset=utf8mb4", "root", "root", [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    echo "<p style='color: green;'>✓ Database connected</p>";
} catch (Exception $e) {
    echo "<p style='color: red;'>✗ Database connection failed: " . $e->getMessage() . "</p>";
    exit;
}

echo "<h3>Step 2: Check User Exists</h3>";
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
$stmt->execute([$email]);
$user = $stmt->fetch();

if ($user) {
    echo "<p style='color: green;'>✓ User found</p>";
    echo "<pre>";
    print_r($user);
    echo "</pre>";
} else {
    echo "<p style='color: red;'>✗ User not found with email: $email</p>";
    
    // Check what emails exist
    $all_users = $pdo->query("SELECT id, email, username FROM users")->fetchAll();
    echo "<h4>All users in database:</h4>";
    foreach ($all_users as $u) {
        echo "<p>{$u['id']}: {$u['email']} ({$u['username']})</p>";
    }
    
    // Create the user
    echo "<h4>Creating admin user...</h4>";
    $hash = password_hash($password, PASSWORD_DEFAULT);
    $create = $pdo->prepare("INSERT INTO users (username, email, password, full_name, is_verified, is_2fa_enabled, created_at, updated_at) VALUES (?, ?, ?, ?, 1, 0, NOW(), NOW())");
    $result = $create->execute(['admin12', $email, $hash, 'Admin User']);
    
    if ($result) {
        echo "<p style='color: green;'>✓ User created</p>";
        $user_id = $pdo->lastInsertId();
        
        echo "<p style='color: green;'>✓ User will be admin (in whitelist)</p>";
        
        // Fetch the user again
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
    }
}

if ($user) {
    echo "<h3>Step 3: Password Verification</h3>";
    echo "<p>Testing password: '$password'</p>";
    echo "<p>Stored hash: " . $user['password'] . "</p>";
    
    $password_ok = password_verify($password, $user['password']);
    echo "<p>Password verification: " . ($password_ok ? '<span style="color: green;">SUCCESS ✓</span>' : '<span style="color: red;">FAILED ✗</span>') . "</p>";
    
    if (!$password_ok) {
        echo "<h4>Fixing password...</h4>";
        $new_hash = password_hash($password, PASSWORD_DEFAULT);
        $update = $pdo->prepare("UPDATE users SET password = ? WHERE email = ?");
        $update->execute([$new_hash, $email]);
        
        // Test again
        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        $password_ok = password_verify($password, $user['password']);
        echo "<p>New password verification: " . ($password_ok ? '<span style="color: green;">SUCCESS ✓</span>' : '<span style="color: red;">FAILED ✗</span>') . "</p>";
    }
    
    echo "<h3>Step 4: Admin Status Check</h3>";
    $admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];
    $is_admin = in_array($email, $admin_emails);
    
    if ($is_admin) {
        echo "<p style='color: green;'>✓ User is in admin whitelist</p>";
        echo "<p>Admin email: $email</p>";
    } else {
        echo "<p style='color: red;'>✗ User not in admin whitelist</p>";
        echo "<p>Available admin emails: " . implode(', ', $admin_emails) . "</p>";
    }
    
    echo "<h3>Step 5: Final Login Test</h3>";
    if ($user && $password_ok && $is_admin) {
        echo "<div style='background: #d4edda; color: #155724; padding: 15px; border: 1px solid #c3e6cb; border-radius: 5px; margin: 20px 0;'>";
        echo "<h4>🎉 LOGIN SHOULD WORK!</h4>";
        echo "<p>✓ User exists</p>";
        echo "<p>✓ Password is correct</p>";
        echo "<p>✓ User has admin privileges</p>";
        echo "</div>";
        
        // Test session setting
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['user_name'] = $user['full_name'];
        $_SESSION['user_email'] = $user['email'];
        $_SESSION['is_admin'] = true;
        $_SESSION['login_time'] = time();
        
        echo "<p><strong>Session set successfully!</strong></p>";
        echo "<p><a href='admin_login.php' style='background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>🚀 Try Admin Login Now</a></p>";
        
    } else {
        echo "<div style='background: #f8d7da; color: #721c24; padding: 15px; border: 1px solid #f5c6cb; border-radius: 5px; margin: 20px 0;'>";
        echo "<h4>❌ LOGIN ISSUES:</h4>";
        echo "<p>User exists: " . ($user ? 'YES' : 'NO') . "</p>";
        echo "<p>Password correct: " . ($password_ok ? 'YES' : 'NO') . "</p>";
        echo "<p>Is admin: " . ($is_admin ? 'YES' : 'NO') . "</p>";
        echo "</div>";
    }
}

echo "<hr>";
echo "<h3>Database Tables Status:</h3>";
echo "<h4>Users table:</h4>";
$users = $pdo->query("SELECT id, email, username, full_name FROM users WHERE email LIKE '%admin%'")->fetchAll();
foreach ($users as $u) {
    echo "<p>{$u['id']}: {$u['email']} - {$u['full_name']}</p>";
}

echo "<h4>Admin whitelist:</h4>";
$admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];
foreach ($admin_emails as $admin_email) {
    echo "<p>✓ $admin_email</p>";
}
?>
