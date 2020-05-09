<?php
include_once('common/base.php');

define('ROSTER_BASE_PATH', 'jmri-data');

function displayFooter(){
    echo '
    <div id="footer">
        <p>JMRI roster v0.1. Source on <a href="https://github.com/wormoworm/jmri-roster">GitHub</a>.</p>
    </div>';
}
?>