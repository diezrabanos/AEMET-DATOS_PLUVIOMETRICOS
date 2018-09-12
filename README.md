# AEMET-DATOS_PLUVIOMETRICOS

Script python2 para recolectar los datos de las 160 estaciones con datos climáticos (temperatura, precipitación y presión)  de la Agencia Estatal de Meteorología (AEMET) de Espàña, en su plataforma AEMET Open Data (https://opendata.aemet.es/centrodedescargas/inicio)
Es necesaria una api key que se puede obtener de forma gratuita registrándose en el siguiente enlace: 
https://opendata.aemet.es/centrodedescargas/altaUsuario

Se incluye tres carpetas comprimidas con los datos en json hasta el 5/09/2018.

¡IMPORTANTE!-->Para posteriores usos se debe descomprimir los archivos zip e incluir TODAS las carpetas en la carpeta JSON_STATIONS. Entonces lanzas con la variable lastyear en 2018 y todos los archivos 2018.json se sobreescriben -aunque iré actualizando para que se pueda simplemente descargar los datos en json de los zips sin hacer peticiones a AEMET-.

Cualquier sugerencia o corrección de código es bienvenida.

Requerimientos: 

Python2

Instalador de paquetes pip --> apt-get install python-pip

beautifullsoup4            --> pip install beautifulsoup4  

*****************************************

Script python2 to collect the data of the 160 stations with pluviometric data from the Spanish Meteorological Agency (AEMET), in its AEMET Open Data platform (https://opendata.aemet.es/centrodedescargas/inicio)
You need an api key that can be obtained for free by registering at the following link:
https://opendata.aemet.es/centrodedescargas/altaUsuario

Three zip files with the data until 9/5/2018 are included.

IMPORTANT!-->For further uses you need to unzip the 160 folders and put them together on JSON_STATIONS folder. Then you can relaunch it with variable lastyear setted at current year and the last year json file of each station will override with all the monthly available data -I will upgrade the zip files with the available data from time to time anyhow, so just download....-.

Required:

Python2

Package manager pip --> apt-get install python-pip

beautifullsoup4     --> pip install beautifulsoup4  
