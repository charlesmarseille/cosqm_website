<!DOCTYPE html>
<html  lang="en" dir="ltr">
<head>
    <meta charset="utf-8">

    <title>Flask App </title>

    <!-- Bootstraps Java Scipts Links -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>



    <!-- JQuery links  -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>


    <!--High CHART LIVE  -->
    <script src="http://code.highcharts.com/highcharts.js"></script>
    <script src="http://code.highcharts.com/highcharts-more.js"></script>
    <script src="http://code.highcharts.com/modules/exporting.js"></script>

    <!--Gauge  -->
    <script type="text/javascript" src="http://pubnub.github.io/eon/lib/eon.js"></script>


</head>

<body>

    <div class="jumbotron">
        <h1 class="text-center text-white">Calculateur d'économies<br> - DH Éclairage - </h1>
    </div>
    <br>
    <br>


    <div class="container-fluid">

        <div class="row">

            <div class="col-5 jumbotron p-2 mx-1">
                <h1 class="sensor1"> Courant : </h1>
            </div>
            <br>

            <div class="col-5 jumbotron p-2 mx-1">
                <h1 class="sensor2"> Puissance :</h1>
            </div>
            <br>



        </div>
    </div>

    <style>

        .jumbotron{
            widows: 150px;
            height: 220px;
            justify-content: center;
        }

        .row{
            justify-content: center;
        }


    </style>

    <div class="container-fluid">
        <!-- Example row of columns -->
        <div class="row">
            <div class="container-fluid" id="data-temperature">

            </div>
        </div>
    </div>
<br>
<br>
<br>

    <div class="container-fluid">
        <!-- Example row of columns -->
        <div class="row">
            <div class="container-fluid" id="data-humidity">

            </div>
        </div>
    </div>


    <script>
        var chartTemperatue;
        var chartHumidity;

        function requestData()
        {
            // Ajax call to get the Data from Flask
            var requests = $.get('/data');

            var tm = requests.done(function (result)
            {
                // Temperature
                var seriesTemperature = chartTemperatue.series[0],
                    shiftTemperature = seriesTemperature.data.length > 20;

                // Humidity
                var seriesHumidity = chartHumidity.series[0],
                    shiftHumidity = seriesTemperature.data.length > 20;

                // Add the Point
                // Time Temperature
                var data1 = [];
                data1.push(result[0]);
                data1.push(result[1]);


                // Add the Point
                // Time Humidity
                var data2 = [];
                data2.push(result[0]);
                data2.push(result[2]);


                chartTemperatue.series[0].addPoint(data1, true, shiftTemperature);
                chartHumidity.series[0].addPoint(data2, true, shiftHumidity);
                $(".sensor1").text("");
                $(".sensor1").text("Courant : " +  Math.round(data1[1]) + "A");

                $(".sensor2").text("");
                $(".sensor2").text("Puissance : " +  Math.round(data2[1]) + "kW");

                // call it again after one second
                setTimeout(requestData, 2000);

            });
        }

        $(document).ready(function()
        {
            // --------------Chart 1 ----------------------------
            chartTemperatue = new Highcharts.Chart({
                chart:
                    {
                    renderTo: 'data-temperature',
                    defaultSeriesType: 'area',
                    events: {
                        load: requestData
                            }
                    },
                title:
                    {
                    text: 'Courant'
                    },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                        },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Courant (A)',
                        margin: 80
                            }
                         },
                series: [{
                    color : '#c23d23',
                    lineColor: '#303030',
                    name: 'Heure',
                    data: []
                }]
            });
            // --------------Chart 1 Ends - -----------------

            chartHumidity = new Highcharts.Chart({
                chart:
                    {
                        renderTo: 'data-humidity',
                        defaultSeriesType: 'area',
                        events: {
                            load: requestData
                        }
                    },
                title:
                    {
                        text: 'Puissance'
                    },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Puissance (kW)',
                        margin: 80
                    }
                },
                series: [{
                    lineColor: '#1d82b8',
                    name: 'Heure',
                    data: []
                }]
            });


        });
    </script>



<script>
    class Image{

        constructor(imgUrl, size)
        {
            this.imgUrl=imgUrl;
            this.size=size;
        }

        backgroundImage()
        {
            console.log("inside function ")
            // Select the Image
            var img = document.querySelector(".jumbotron");

            // create Css Text
            var text = "margin:auto;"+
                "background-image: url("+this.imgUrl+");" +
                "background-size:cover;"+
                "opacity:1;"+
                "background-blend-mode: darken;"+
                "height: "+ this.size + "vh;";

            img.style.cssText =  text;
        }

        centerTitle()
        {
            /*
                Center the Title
             */
            var t1 = document.querySelector("#title");
            t1.classList.add("text-white");
            t1.classList.add("text-center");
            t1.classList.add("display-3");
        }
    }

    const imgUrl = '/static/Thunder_Electricity_With_sfx_-_Free_HD_Footage.gif'
    const size = "40";
    var obj = new Image(imgUrl, size);
    obj.backgroundImage();
    obj.centerTitle();
    </script>
</body>


</html>
