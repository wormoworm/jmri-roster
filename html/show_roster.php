<?php
include('ui_base.php');
include_once('common/loader.php');

function getPageTitle(){
    return 'Roster';
}

$loader = new Loader(ROSTER_BATH_PATH);
$roster = $loader -> loadRoster();
?>

<!DOCTYPE html>
<html>
    <head>
        <title><?php echo getPageTitle(); ?></title>
    </head>
    <body>
        <h1 id="title"><?php echo getPageTitle(); ?></h1>
        <p><?php echo 'The roster contains '.$roster->getLocomotiveCount().' locomotives, and was last updated on '.getFriendlyDate($roster->modified).' at '.getFriendlyTime($roster->modified).'.';?></p>
        <table id="locomotives">
            <tr>
                <th>ID</th>
                <th>Address</th>
                <th>Model</th>
                <th>Owner</th>
                <th></th>
            </tr>
<?php
foreach($roster->locomotives as $locomotive){
    echo
    '<tr>
        <td>'.$locomotive->id.'</td>
        <td>'.$locomotive->dccAddress.'</td>
        <td>'.$locomotive->model.'</td>
        <td>'.$locomotive->owner.'</td>
        <td><a href="locomotive/'.$locomotive->id.'">View</a></td>
    </tr>';
}
?>
        </table>
    <?php displayFooter(); ?>
    </body>
</html>