import os

fileString = \
"<html>\n"\
+"  <head>\n"\
+"    <style>\n"\
+"      body{\n"\
+"        background-image: url('utils/gifs/AnnMargret_hot_dance_with_Elvis_Presley_in_Viva_Las_Vegas_4.gif');\n"\
+"        background-size:100%;\n"\
+"        background-attachment: fixed;\n"\
+"        height:100%;\n"\
+"        width:100%;\n"\
+"        background-position: center;\n"\
+"        filter: blur(2px);\n"\
+"        backdrop-filter: blur(1px);\n"\
+"      }\n"\
+"    </style>\n"\
+"    <link href=\"http://fonts.cdnfonts.com/css/kabel\" rel=\"stylesheet\">\n"\
+"    <script type=\"text/javascript\">\n"\
+"      const listOfGifs = <listOfGifs>;\n"\
+"      function run(){\n"\
+"        var fileName = \"\";\n"\
+"        fileName = listOfGifs[Math.floor(Math.random()*listOfGifs.length)];\n"\
+"        document.body.style.backgroundImage = \"url('utils/gifs/\"+fileName+\"')\";\n"\
+"        window.setTimeout(function(){ document.location.reload(true); }, 15000);\n"\
+"        //setTimeout(run,15000)\n"\
+"        //document.getElementById(\"target\").innerHTML = \"ran\";\n"\
+"        //document.body.style.backgroundImage = \"url('utils/gifs/AnnMargret_hot_dance_with_Elvis_Presley_in_Viva_Las_Vegas_4 (1).gif')\";\n"\
+"      }\n"\
+"    </script>\n"\
+"  </head>\n"\
+"  <body onload=\"run()\" style=\"background-color:Black;\">\n"\
+"    <p id=\"target\" style=\"text-shadow: -4px 4px black; font-family: 'Kabel', sans-serif; font-size:25; color:white;position: fixed; bottom: 0; text-align: left\">artist-song<br>dj-show</p>\n"\
+"  </body>\n"\
+"</html>"
fileString = fileString.replace('<listOfGifs>',str(os.listdir('utils/gifs/')))

file = open('visuals_template.html','w+')
file.write(fileString)
file.close()