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

function outputLocomotiveRow($locomotive){
    $thumbnailSize = 200;
    $imagePath = areURLRewritesAvailable() ? 'api/v1/locomotive/'.$locomotive->id.'/image/'.$thumbnailSize : '/api/v1/api_locomotive_image.php?locomotive_id='.$locomotive->id.'&amp;width='.$thumbnailSize;
    $link = getLocomotiveDetailLink($locomotive);
    echo '
    <div class="locomotiveRow contentBlock">
        <a href="'.$link.'">
            <div class="locomotiveThumbnail">';
            if($locomotive->hasImage()){
                echo '
                <img src="'.$imagePath.'" />';
            }
        echo
        '
            </div>
            <div class="textContent">
                <h3 class="locomotiveNumber">'.$locomotive->number.'</h3>
                <p class="locomotiveName">'.$locomotive->name.'</p>
                <p class="locomotiveAddress">Address:<span class="addressValue">'.$locomotive->dccAddress.'</span></p>
            </div>
        </a>
    </div>';
}

$loader = new Loader(ROSTER_BASE_PATH);
$roster = $loader -> loadRoster();
?>

<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <title><?php echo getPageTitle(); ?></title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    </head>
    <body>
        <div id="content">
            <div class="contentHorizontalPadding">
                <h1 id="title"><?php echo getPageTitle(); ?></h1>
                <p id="subtitle"><?php echo 'The roster contains '.$roster->getLocomotiveCount().' locomotives, and was last updated on '.getFriendlyDate($roster->modified).' at '.getFriendlyTime($roster->modified).'.';?></p>
            </div>
    <?php
    $n = 0;
    foreach($roster->locomotives as $locomotive){
        outputLocomotiveRow($locomotive);
    }
    ?>
            </table>
        <?php displayFooter(); ?>
    </div>
    </body>
</html>