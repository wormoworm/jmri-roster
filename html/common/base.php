<?php
ini_set('display_errors', '1');

$GLOBALS['DEVELOPMENT_SERVER'] = isset($_SERVER['SERVER_SOFTWARE']) && strpos($_SERVER['SERVER_SOFTWARE'], 'Development Server')!==FALSE;
?>