<!DOCTYPE html>
<html  lang="en" dir="ltr">
<head>
    <meta charset="utf-8">

    <title>Flask App </title>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Add icon library -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    .btn {
      background-color: DodgerBlue;
      border: none;
      color: white;
      padding: 12px 30px;
      cursor: pointer;
      font-size: 20px;
    }
    
    /* Darker background on mouse-over */
    .btn:hover {
      background-color: RoyalBlue;
    }
</style>

</head>

    <!-- Bootstraps Java Scipts Links -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>


<body>

    <div class="jumbotron">
        <h1 class="text-center text-white">CoSQM - Multispectral SQM hack -</h1>
    </div>
    <br>

    <style>
        .jumbotron{
            widows: 150px;
            height: 100px;
            justify-content: center;
        }

        .row{
            justify-content: center;
        }
    </style>



    <form action="/" method="POST">
    <!-- choose the station from available cosqm instruments locations -->
    <label for="station_name">1. Choose a Station:</label>
    <select name="station_name">
        <option value="Santa-Cruz_Tenerife" {% if station_name == 'Santa-Cruz_Tenerife' %} selected {% endif %}>Santa-Cruz_Tenerife</option>
	<option value="COU-Montsec" {% if station_name == 'COU-Montsec' %} selected {% endif %}>COU-Montsec</option>
	<option value="Izana_AEMET" {% if station_name == 'Izana_AEMET' %} selected {% endif %}>Izana_AEMET</option>
        <option value="Observatorio_Teide" {% if station_name == 'Observatorio_Teide' %} selected {% endif %}>Observatorio_Teide</option>
        <option value="Pico_Teide" {% if station_name == 'Pico_Teide' %} selected {% endif %}>Pico_Teide</option>
        <option value="Saint-Camille" {% if station_name == 'Saint-Camille' %} selected {% endif %}>Saint-Camille</option>
        <option value="UCMadrid" {% if station_name == 'UCMadrid' %} selected {% endif %}>UCMadrid</option>
    </select>
    <br>

    <!-- choose the date from all days of the year -->
    <label for="date">2. Choose 1 or 2 adjacent dates (YYYY-MM-DD):</label>
    {% if name != '2020-01-01' %}
        <input name="date" value={{ date }}>
        <input name="date2" value={{ date2 }}>
    {% else %}
    {% endif %}

    <input type='submit' value='GRAPH'>
    <br>

    <label for="filters">3. Choose the filter colors to display:</label>
    <input type="checkbox" {% if d.C %} checked {% endif %} name="C" value="1">
    <label for="C"> C</label>
    <input type="checkbox" {% if d.R %} checked {% endif %} name="R" value="1">
    <label for="R"> R</label>
    <input type="checkbox" {% if d.G %} checked {% endif %} name="G" value="1">
    <label for="G"> G</label>
    <input type="checkbox" {% if d.B %} checked {% endif %} name="B" value="1">
    <label for="B"> B</label>
    <input type="checkbox" {% if d.Y %} checked {% endif %} name="Y" value="1">
    <label for="Y"> Y</label>
    </form>
    <br>

    <!-- Show chosen station and date -->
    {% if d.graph_state != 0 %}
        {% if err == 'err1' %}
            <h2>Date 1 does not exist!</h2>
        {% elif err == 'err2' %}
            <h2>Date 2 does not exist!</h2> 
        {% else %}
            <h5>Showing -> {{ station_name }}{{ date }} - {{ date2 }}{{ filters }}</h5>
            <!-- Show graph of the selected station and date -->
	    <img src="static/{{ filename }}" alt="{{ filename }}">
        {% endif %}
    {% else %}
    {% endif %}
    <br>


    <label>(right-click to save figure)</label>
    <br>
    <a href="static/{{ filename[:-4] }}.txt" download>
        <button class="btn"><i class="fa fa-download"></i> Download graph data</button>
    </a>


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

        const imgUrl = '/static/light_pollution.png'
        const size = "30";
        var obj = new Image(imgUrl, size);
        obj.backgroundImage();
        obj.centerTitle();
    </script>

</body>


</html>
