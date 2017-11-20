Introducción
============

Motivación
----------

El análisis de datos es una tarea que se ha extendido rápidamente por las empresas modernas. Hoy en día nadie niega el valor que aportan los datos al conocimiento interno al desarrollo de negocio. La tecnología a nuestra disposición nos facilita la captura de datos y su procesamiento, aunque el tamaño de los mismos parezca inmanejable. Por otro lado una gran cantidad de librerías científicas nos permiten hacer maravillas con los datos que tenemos en nuestra máquina, siempre que entren en la memoria de la máquina.

> Pero no puedo evitar pensar en este vacío intermedio entre el trabajo en local y el trabajo en grandes centros de proceso. Y lo visualizo como un valle yermo.

Que inevitablemente tenemos que recorrer cada vez que una hipótesis prometedora debe ser llevada al mundo real. Yo llamo a este trabajo **el valle de la soledad**. La popularidad entre los científicos de datos de las librerías más enfocadas al procesamiento local, que agilizan su trabajo, provocan en la mayoría de los casos un esfuerzo considerable cuando las intentamos encajar en el cluster; en muchas ocasiones en mi carrera profesional me he encontrado traduciendo código en R o Python a Java o Escala. No porque el lenguaje en sí sea determinante, sino porque es el que usa el framework de procesamiento big data que típicamente tiene el cliente instalado en sus servidores.

En mi opinión cuanto más pequeñas y sencillas sean las operaciones de transformación de datos más sencillo es el paso por el valle de la soledad. Con la inclusión de Python en Spark se abre además la puerta de usar el mismo lenguaje (aunque el código pueda variar).

Soluciones
~~~~~~~~~~

Mucha gente a la que le pregunto cómo está solucionando su viaje por el valle de la soledad usa directamente los frameworks big data en la máquina de desarrollo local. Es una opción totalmente respetable, pero tiene un coste asociado, en mi opinión bastante limitante. Cada vez que llevamos a cabo una prueba debemos pagar el peaje del framework; que no es más que la infraestructura que monta para ofrecerte una escalabilidad que no estas usando, y que muy probablemente no usarás, ya que muchas de las hipótesis que se están probando no llegarán nunca a producción.
Otra opción popular es la de usar los datos y el cluster de verdad. Pero eso también tiene un coste asociado alto; puede impactar en procesos productivos, si no tienes duplicada la información e infraestructura; y para mayor dificultad los cluster y frameworks big data están diseñados para exprimir al máximo los recursos y no responden bien a la pugna de recursos típica de un sistema multiusuario.

No hay una solución sencilla o general para este problema, y cada problema tiene sus peculiaridades que pueden invalidar totalmente una aproximación. Por ejemplo, quiero desarrollar con el cluster real, pero hay tantos datos que hace que cada prueba me lleve días. O hay muy pocos datos pero estoy obligado a escribir mi código de nuevo porque el cluster usa la tecnología X.

En mi opinión el único paliativo a este problema es ser lo más progresivo y automatizar para no tener que parar el trabajo de investigación del científico de datos por culpa de la tecnología. Cuando digo progresivo me refiero a que nuestro código tenga la capacidad de ser expuesto a cantidades cada vez mayores de datos de forma desatendida y que el científico de datos pueda consultar las métricas de desempeño y decidir si se progresa ese modelo para ser expuesto a más datos o no. La automatización debe permitir el manejo, selección y exposición de los datos a los modelos sin intervención humana. No solo para alcanzar mayor productividad, sino que esto permite una mayor seguridad de los datos.

>  En este punto se hace evidente la necesidad de un buen pipeline de datos.

Apoyo en lo existente, no sustitución
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si queremos tener éxito y ser competitivos necesitamos que nuestras estrategias sean rápidas y económicas. Y en el caso de la transformación de datos debemos apuntar a generar código que no sea ya facilitado por frameworks (que hacen muy bien esta tarea). Los frameworks de big data facilitan sobretodo el mover los datos de un sitio a otro; por ejemplo, leer de un csv y hacer un join con los datos de un Cassandra para alimentar un Elastic Search.

> Pero cuando queremos añadir un campo, o dividir una fecha entre sus campos individuales, queda totalmente en nuestras manos.

De una forma similar las librerías científicas también te ayudan a cargar ficheros y a pintar gráficas. Pero cuando tenemos que hacer operaciones sobre campos, de nuevo, recae sobre nuestro código.

Y es precisamente este código el que tediosamente provoca más trabajo. Dando lugar al valle de la soledad, cuando tenemos que estar adaptando código para pasar de un framework a otro, solos, sin ayuda alguna. La librería ETL viene a facilitarnos la vida con una base de código que podemos usar en cualquier punto del proceso. Aunque no siendo una solución completa, si que ha demostrado reducir el tiempo necesario para llevar a cabo los ELT necesarios y reducir drásticamente el tiempo necesario para adaptar el código de los frameworks locales al cluster de producción.

Esto se consigue mediante el interfaz minimalista que usa. En lugar de pretender ser una solución global (como spark que cada vez aúna más funcionalidad) simplemente te entrega una sola función de código a la que le pasas los datos y te da los datos transformados en base a los metadatos que se le provee. Esto implica que la solución deja al framework el dimensionamiento, mientras que la función solo se preocupa de transformar los datos.

Enfocado desde el streaming
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Esta decisión de diseño puede resultar muy alienante a aquellos más experimentados con soluciones ETL completas. En ocasiones me encuentro con comentarios como: “donde le paso los datos” o “como puedo recorrer una columna”. Para resolver este tipo de dudas debemos recordar que la librería trabaja a nivel de fila, o como se describe en las aplicaciones en streaming, a nivel de un solo evento. Un fichero normalmente está compuesto por muchos eventos, a si que tienes que extraer los eventos uno por uno y pasarlos por la función que te entrega la librería para obtenerlos transformados.

Como hemos explicado la librería no va a abordar las tareas que ya hacen los frameworks especializados; porque lo hacen mejor de lo que podemos pretender nosotros. Pandas, por ejemplo, te permite cargar un fichero con una solo línea de código, y Spark también; te recomiendo usar uno de estos frameworks y mapear las filas con la función de la librería.

En la cuestión de columna también hay cierta confusión, creo que debido a la forma común de trabajar con los datos que vienen estableciendo los dataframes en los últimos años. Estos son estructuras columnares, muy adecuados y eficientes cuando tenemos un fichero finito y completo de datos entre manos. Pero la librería de ETL, de nuevo, trabaja a nivel de evento, aproximación opuesta en principio al paradigma columnar, por lo que a priori implica un pequeño cambio de enfoque para los datascientist.

> Trabajar pensando en los eventos y no en las columnas de datos.

Y está limitado en este aspecto porque está diseñado desde la suposición de que todos los datos son stream infinitos; lo que permite el poder pasar los datos de forma progresiva; también permite el ahorro de una gran cantidad de recursos de la máquina facilitando su uso en la máquina local o en entornos con los recursos limitados; y también ofrece una solución que funciona en streaming, de modo que es más sencillo de usar en entornos productivos, al mismo tiempo de que se puede usar como un batch tradicional con un pipe de linux.

