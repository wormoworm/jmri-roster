<?php
include('ui_base.php');
include_once('common/loader.php');

$loader = new Loader(ROSTER_BATH_PATH);
$locomotives = $loader -> loadRoster();

# TODO Output a nice table.
print_r($locomotives);
?>