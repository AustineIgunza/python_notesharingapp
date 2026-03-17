<?php
echo "<h2>Redirect Path Test</h2>";

echo "<h3>Current Location:</h3>";
echo "<p>Current file: " . __FILE__ . "</p>";
echo "<p>Current directory: " . __DIR__ . "</p>";
echo "<p>Document root: " . $_SERVER['DOCUMENT_ROOT'] . "</p>";

echo "<h3>Redirect Paths from admin_login.php:</h3>";
echo "<p>Relative path: <code>admin/dashboard.php</code></p>";
echo "<p>This should resolve to: <code>views/admin/dashboard.php</code></p>";

echo "<h3>Testing Paths:</h3>";
$test_paths = [
    'admin/dashboard.php',
    './admin/dashboard.php', 
    '../admin/dashboard.php',
    'views/admin/dashboard.php'
];

foreach ($test_paths as $path) {
    $full_path = __DIR__ . '/' . $path;
    $exists = file_exists($full_path);
    echo "<p><strong>$path:</strong> " . ($exists ? '✅ EXISTS' : '❌ NOT FOUND') . "</p>";
    if ($exists) {
        echo "<p style='margin-left: 20px;'>Full path: $full_path</p>";
    }
}

echo "<h3>Direct Links to Test:</h3>";
echo "<p><a href='admin/dashboard.php' target='_blank'>→ admin/dashboard.php</a></p>";
echo "<p><a href='./admin/dashboard.php' target='_blank'>→ ./admin/dashboard.php</a></p>";
echo "<p><a href='../admin/dashboard.php' target='_blank'>→ ../admin/dashboard.php</a></p>";

echo "<hr>";
echo "<p><a href='admin_login.php'>← Back to Admin Login</a></p>";
?>
