<?php
/**
 * Admin Middleware
 * Ensures only admin users can access admin pages
 */

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header('Location: ../auth/signin.php');
    exit();
}

// Check admin status using whitelist approach (more reliable)
$user_email = $_SESSION['user_email'] ?? '';
$admin_emails = ['admin12@gmail.com', 'austineigunza@gmail.com'];

// Also check if session already has admin flag set
$is_session_admin = isset($_SESSION['is_admin']) && $_SESSION['is_admin'] === true;

if (!$is_session_admin && !in_array($user_email, $admin_emails)) {
    // User is not an admin, redirect to regular dashboard
    error_log("AdminMiddleware: Access denied for $user_email");
    header('Location: ../dashboard.php');
    exit();
}

// Set admin flag in session if not already set
if (!$is_session_admin && in_array($user_email, $admin_emails)) {
    $_SESSION['is_admin'] = true;
    error_log("AdminMiddleware: Admin access granted for $user_email");
}
