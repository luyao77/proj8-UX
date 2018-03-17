<html>
    <head>
        <title> Consumer for Testing
         </title>
         </head>

    <body>
      <ul>
        <h1>ListAll</h1>

            <?php
            $json = file_get_contents("http://laptop-service/listAll");

            $obj = json_decode($json);
            $open_time = $obj->open_time;
            $close_time = $obj->close_time;

            echo "  Open:\n";
            foreach ($open_time as $l) {
                echo "<li>$l</li>";
            }
            echo "  Close:\n";
            foreach ($close_time as $l) {
                echo "<li>$l</li>";
            }

            ?>
        <h1>ListOpenOnly</h1>
            <?php
             $json = file_get_contents('http://laptop-service/listOpenOnly');
             $obj = json_decode($json);
             $open_time = $obj -> open_time;


             foreach ($open_time as $l) {
                 echo "<li>$l</li>";
             }
             ?>
        <h1>ListCloseOnly</h1>
            <?php
             $json = file_get_contents('http://laptop-service/listCloseOnly');
             $obj = json_decode($json);
             $open_time = $obj -> close_time;



             foreach ($close_time as $l) {
                 echo "<li>$l</li>";
             }
             ?>
        <h1>Json listAll </h1>
            <?php
                 $json = file_get_contents("http://laptop-service/listAll/json");

                 $obj = json_decode($json);
                 $km = $obj->km;
                 $open_time = $obj->open_time;
                 $close_time = $obj->close_time;

                 echo "  Km:\n";
                 foreach ($km as $l) {
                     echo "<li>$l</li>";
                 }
                 echo "  Open Time:\n";
                 foreach ($open_time as $l) {
                     echo "<li>$l</li>";
                 }
                 echo "  Close Time:\n";
                 foreach ($close_time as $l) {
                     echo "<li>$l</li>";
                 }

               ?>
        <h1>Json OpenOnly</h1>
            <?php
             $json = file_get_contents('http://laptop-service/listOpenOnly/json');
             $obj = json_decode($json);
             $open_time = $obj -> open_time;



             foreach ($open_time as $l) {
                 echo "<li>$l</li>";
             }
             ?>
        <h1>Json CloseOnly</h1>
            <?php
             $json = file_get_contents('http://laptop-service/listCloseOnly/json');
             $obj = json_decode($json);
             $close_time = $obj -> close_time;
             // $km = $obj -> km;
             //
             //
             // echo "  Km:\n";
             // foreach ($km as $l) {
             //     echo "<li>$l</li>";
             // }

             foreach ($close_time as $l) {
                 echo "<li>$l</li>";
             }
             ?>

        <h1>CSV  listAll </h1>
            <?php

             echo file_get_contents('http://laptop-service/listAll/csv')
             ?>
        <h1>CSV OpenOnly</h1>
            <?php

             echo file_get_contents('http://laptop-service/listOpenOnly/csv')
             ?>
        <h1>CSV CloseOnly</h1>
            <?php

             echo file_get_contents('http://laptop-service/listCloseOnly/csv')
             ?>
        <h1>Top = 3 Open Time in CSV</h1>
            <?php
            echo file_get_contents('http://laptop-service/listOpenOnly/csv?top=3');
            ?>

        <h1>Top = 3 Open Time in Json</h1>
            <?php
            $json =  file_get_contents('http://laptop-service/listOpenOnly/json?top=3');
            $obj = json_decode($json);
            $open_time = $obj -> open_time;

            foreach ($open_time as $l) {
              echo "<li>$l</li>";
            }
            ?>



    </ul>

  </body>
</html>
