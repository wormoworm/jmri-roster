<?php
include('ui_base.php');
include_once('common/loader.php');

$loader = new Loader(ROSTER_BATH_PATH);
$locomotive = $loader -> loadLocomotive($_GET['locomotive_id']);

# TODO Output a nice table with loco image.
print_r($locomotive);
?>