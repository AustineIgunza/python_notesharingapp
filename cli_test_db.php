<?php
require_once 'config/conf.php';
require_once 'app/Services/Global/Database.php';

echo "Creating Database object...\n";
try {
    $db = new Database($conf);
    echo "Database created successfully\n";
    echo "Stub mode: " . ($db->isStubMode() ? 'YES' : 'NO') . "\n";
    if (!$db->isStubMode()) {
        echo "Testing query...\n";
        $result = $db->fetchOne('SELECT 1 as test');
        echo "Query result: " . json_encode($result) . "\n";
    }
} catch (Exception $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . ":" . $e->getLine() . "\n";
}
?>
