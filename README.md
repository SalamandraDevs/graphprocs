# graphprocs
Grafica los procesos de tu servidor en el navegador web.

## Instalar
Primero clona el respositorio y ejecuta `cd graphprocs`.

Asegúrate de tener un entorno virtual de python, el cual puedes configurar con 
`python3 -m venv ./`

Esto hará que todo quede dentro de `graphprocs/bin` luego activa el entorno con `source bin/activate`, luego instala las dependencias con `bin pip install flask matplotlib psutil`

Ahora sí ejecuta `python main.py` y con eso puedes ir a `localhost:5000` para ver el gráfico actualizarse cada intervalo. Con esto puedes hacer un proxy forward para servirlo desde tu servidor y ver los gráficos desde tu casa.


