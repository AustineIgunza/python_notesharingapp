<?php
echo "<h2>Path Resolution Test from Views Directory</h2>";

echo "<h3>Current Working Directory:</h3>";
echo "<p>" . getcwd() . "</p>";

echo "<h3>File Existence Check:</h3>";
$files_to_check = [
    '../config/conf.php',
    '../app/Services/Global/Database.php',
    '../app/Services/Global/fncs.php'
];

foreach ($files_to_check as $file) {
    $full_path = realpath($file);
    if (file_exists($file)) {
        echo "<p style='color: green;'>✓ $file exists</p>";
        echo "<p style='margin-left: 20px;'>Full path: $full_path</p>";
    } else {
        echo "<p style='color: red;'>✗ $file NOT FOUND</p>";
    }
}

echo "<h3>Configuration Loading Test:</h3>";
try {
    require_once '../config/conf.php';
    echo "<p style='color: green;'>✓ Config loaded successfully</p>";
    echo "<p>DB Name: " . $conf['db_name'] . "</p>";
    echo "<p>DB Host: " . $conf['db_host'] . "</p>";
    echo "<p>DB User: " . $conf['db_user'] . "</p>";
} catch (Exception $e) {
    echo "<p style='color: red;'>✗ Config load failed: " . $e->getMessage() . "</p>";
}

echo "<h3>Database Class Loading Test:</h3>";
try {
    require_once '../app/Services/Global/Database.php';
    echo "<p style='color: green;'>✓ Database class loaded successfully</p>";
    
    $db = new Database($conf);
    echo "<p style='color: green;'>✓ Database object created successfully</p>";
    echo "<p>Stub mode: " . ($db->isStubMode() ? 'YES' : 'NO') . "</p>";
    
} catch (Exception $e) {
    echo "<p style='color: red;'>✗ Database class failed: " . $e->getMessage() . "</p>";
}

echo "<hr>";
echo "<p><a href='dashboard.php'>← Try Dashboard</a></p>";
?>
