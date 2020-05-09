<?php
include('ui_base.php');
include_once('common/loader.php');

function getPageTitle(){
    return 'Roster';
}

function getLocomotiveDetailLink($locomotive){
    if(isDevelopmentServer()) return 'show_locomotive_details.php?locomotive_id='.$locomotive->id;
    else return 'locomotive/'.$locomotive->id;
}

$loader = new Loader(ROSTER_BASE_PATH);
$roster = $loader -> loadRoster();
?>

<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <title><?php echo getPageTitle(); ?></title>
    </head>
    <body>
        <div id="content">
            <h1 id="title"><?php echo getPageTitle(); ?></h1>
            <p id="subtitle"><?php echo 'The roster contains '.$roster->getLocomotiveCount().' locomotives, and was last updated on '.getFriendlyDate($roster->modified).' at '.getFriendlyTime($roster->modified).'.';?></p>
            <table id="locomotives" cellspacing="0" cellpadding="0">
                <tr>
                    <th>Number</th>
                    <th>Name</th>
                    <th>Address</th>
                    <th>Owner</th>
                </tr>
    <?php
    $n = 0;
    foreach($roster->locomotives as $locomotive){
        $link = getLocomotiveDetailLink($locomotive);
        echo
        '<tr class="'.($n++ % 2 == 1? 'odd' : 'even').'">
            <td><a href="'.$link.'"><p>'.$locomotive->number.'</p></a></td>
            <td><a href="'.$link.'"><p>'.$locomotive->name.'</p></a></td>
            <td><a href="'.$link.'"><p>'.$locomotive->dccAddress.'</p></a></td>
            <td><a href="'.$link.'"><p>'.$locomotive->owner.'</p></a></td>
        </tr>';
    }
    ?>
            </table>
        <?php displayFooter(); ?>
    </div>
    </body>
</html>