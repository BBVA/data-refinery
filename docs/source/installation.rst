Instalación
============

Requisitos
----------

Para poder instalar datarefinery es necesario:

- Python 3.6

Pip
~~~

Para instalar datarefinery con pip:

.. code-block:: bash

    pip install datarefinery


Docker
~~~~~~

También puedes generar un contenedor para usar la librería con notebooks (debes cumplir también los requisitos anteriores):

.. code-block:: bash

    ./make_container.sh
    docker run -it --rm -p 8888:8888 datarefinery-notebook:latest
