The Basics
==========

Operaciones por campo
---------------------

**TODO: explicar cómo construimos la narrativa desde el campo a un proceso completo.**

El campo como raíz del cambioUn ETL se compone de un conjunto de operaciones sobre una fila. Las filas están compuestas por conjuntos de campos. De forma que la operación mínima que podemos llevar a cabo pasa en un campo.

Supongamos una función no hace nada aplicada al campo V:![None function.jpg](https://lh3.googleusercontent.com/KZ1MTv9z3QagVn_Gn5D4Jj7ZfPgcugdL1aIN-Mv63YY_hupDKqjqur4ZAOL3jXiEfXSoKsj5QuANVyrm14HHrTuAK2oJGIQcxUPzQGMT_WXlnTEyuqqSTss1cJSxoaBRqQu-XL96)Como el proceso está compuesto por operaciones sobre los campos si aplicamos esta función, a una fila que solo tiene el campo V, no obtendremos ninguna salida.

De esta forma llegamos hasta la primera función necesaria, mantener el valor de un campo. Para mantener el valor necesitamos un función que devuelva lo que reciba, típicamente esta función es conocida como identidad:![función identidad.jpg](https://lh3.googleusercontent.com/wCpoosG-B8hIWrrjHDiG8nZV2riGoIamZrQHwMa2WrOa1DFcKJJgqjJQYq6JNEoEat2F3iBwAoEuIlJjG1RjjBSa4v1IfxRDXEJ2GYLF6oZRwYnmcOmxtJboQXdrBDNe3s3OGPeC)

Una función que pueda fallar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dentro de las situaciones que nos encontramos durante una transformación de datos debemos enfrentarnos a los errores. Un problema típico de trabajar con datos, sobretodo cuando no pertenecen a una fuente de datos estructurados, es que alguno de los campos que esperamos no esté ahí. En el caso de que no podamos llevar a cabo una transformación, ya sea por cuestiones internas al campo o por errores externos al proceso, debemos informar de la forma más precisa posible y sin detener el proceso. La información de porque no se ha podido procesar un campo debe agregarse a los fallos que puedan tener otros campos, es decir, que no debemos detener el procesamiento de la fila por un campo. De esta forma el científico de datos puede tener una lista completa con todas las cosas a las que debe enfrentarse. De forma similar debemos seguir procesando el dataset aunque una fila no haya podido ser procesada. En este caso no debemos parar de procesar debido a que en producción es común ver datos para los que el modelo no está preparado, en este caso la fila debe ser descartada junto con los motivos de porque esto es así; de esta forma podremos adaptar el ETL a estos cambios en el próximo entrenamiento.

Para solucionar este problema, lo que hacemos es que las funciones para transformar un campo devuelven el posible valor y también el posible error. Esto nos lleva a tres posibles escenarios:

- La función devuelve un valor y ningún error
- La función devuelve un error, y provoca que nos de lo mismo el valor.
- La función no falla, pero tampoco de un valor.

En el primer caso podremos usar el valor modificado.
En el segundo caso nos da lo mismo el valor, ya que hay un error que no nos permite seguir.
En el tercer caso depende de la operación que estemos haciendo, descartaremos el campo o fallaremos al no tener valor.

Listado de funciones
~~~~~~~~~~~~~~~~~~~~

El ETL suele pelearse con problemas recurrentes de formato de los datos. Transformar tipos, el cambiar valores si cumplen cierta condición, descomponer datos en sus integrantes… Por eso la librería tiene ya algunas funciones muy comunes ya definidas. También podemos crear nuestras propias funciones, si las existentes no cumplen los requisitos. Y para dar soporte a casos más complejos podemos “encadenar” varias funciones más sencillas, permitiendo un uso atómico por pasos pequeños y posibilitando el cambiar fácilmente la funcionalidad intercalando funciones muy sencillas en un proceso. Una gran mayoría de las funciones de ETL ya definidas necesitan unos parámetros de contexto y con estos construirán y devolverán una función que nos permita llevar a cabo la transformación de campo sin estar pasando un número variable de argumentos. Lo que al fin y al cabo permite la composición sencilla, al compartir todas las funciones la misma entrada y salida en todos los pasos.

Reforzando un tipo
..................

En ocasiones la fuente de datos no contiene información de tipo, o esta no es correcta, y nos llegan números como textos, o similar. Esta función necesita como contexto la función que permite el cambio del tipo, si esta función da algún error supondrá que no puede llevar a cabo la transformación y usará el mensaje de error de la excepción como resultado de error.

Por ejemplo, si quiero cambiar el tipo de un dato a int puedo usar el siguiente código:

.. code-block:: python
    from datarefinery.FieldOperations import type_enforcer

    int_enforcer = type_enforcer(lambda x: int(x))
    (res, err) = int_enforcer("6")
    print(res) # 6

Normalización min max
.....................

Esta es una operación típica en machine learning. Consiste en interpolar entre 0 y 1 un valor, considerando que el 0 es representado por el valor min y el 1 es representado por el valor max. Esta función necesita el mínimo y el máximo como contexto para su creación. Un ejemplo de uso podría ser:

.. code-block:: python
    from datarefinery.FieldOperations import min_max_normalization

    normalizator = min_max_normalization(1, 10)
    (res, err) = normalizator(5)
    print(res) # 0.5

Puntuación estandar
...................

Esta operación representa lo lejos que está un dato de la estadística representativa de una columna completa. Para usarlo necesitamos pasarle como contexto la media y la desviación típica de los valores de la columna. Un ejemplo de uso sería:

.. code-block:: python
    from datarefinery.FieldOperations import std_score_normalization

    normalizator = std_score_normalization(79, 8)
    (res, err) = normalizator(85)
    print(res) # 0.75

Agrupando por valor
...................

Esta función nos ayuda cuando queremos convertir un valor lineal numérico en uno categórico. Un caso común de uso es agrupar usuarios por edad. Requiere como contexto el paso de al menos un valor, esto generará dos grupos uno desde menos infinito al valor y del valor hasta infinito.

Continuando con el ejmplo de edad, si queremos distinguir entre niños, adultos y jubilados podríamos pasar como valores 18 y 70. De esta forma la agrupación generará los siguientes grupos:

1. Entre menos infinito y 18
2. Entre 18 y 70
3. Entre 70 e infinito

En código podríamos ver estas situaciones así:

.. code-block:: python
    from datarefinery.FieldOperations import buckets_grouping

    group = buckets_grouping(18, 70)
    (res, err) = group(10)
    print(res) # 1
    (res, err) = group(20)
    print(res) # 2
    (res, err) = group(73)
    print(res) # 3

Categorización lineal
.....................

Esta operación de campo cambia los datos categóricos, como textos, en un número. Para ellos debemos pasarle las categorías existentes siempre con los elementos en las mismas posiciones (añadiendo siempre al final los nuevos valores).
Esto se debe a que asignará el valor numérico del orden de la lista, y necesitamos que sea coherente entre ejecuciones.

Como ejemplo podemos categorizar de nuevo la edad, pero esta vez nos llega como texto en lugar de como número.

.. code-block:: python
    from datarefinery.FieldOperations import linear_category

    categorizer = linear_category(["niño", "adulto", "jubilado"])
    (res, err) = categorizer("adulto")
    print(res) # 2

Categorización columnar
.......................

Funciona como la categorización lineal pero genera una columna con cada valor de la categoría, por defecto tendrá valor de 0, y en la categoría encontrada en el campo tendrá 1. También es conocido como *one hot vector*.

Continuando con el ejemplo de la edad.

.. code-block:: python
    from datarefinery.FieldOperations import column_category

    categorizer = column_category(["niño", "adulto", "jubilado"])
    (res, err) = categorizer("niño")
    print(res) # {"niño": "1", "adulto": "0", "jubilado": "0"}

Esta operación añade campos, por lo que suele usarse con una operación de evento de tipo [append](##Cange it).

Prefijo de columna
..................

En casos en los que una función genera varios campos es posible que estas coincidan en nombre con otros campos. Por eso podemos usar esta función que añadirá un prefijo al nombre de la columna.

.. code-block:: python
    from datarefinery.FieldOperations import add_column_prefix

    prefix = add_column_prefix("good")
    (res, err) = prefix({"one": "me"})
    print(res) # {"good_one": "me"}

Deconstrucción de campos
........................

Es común encontrar datos anidados, la función explode aplana esta anidación, incluso si esta está formada por una lista de objetos.
En el caso de que haya un solo sub objeto no se añadirá más que el prefijo del nombre de campo original. Pero si hay una lista con varios elementos entonces al nombre del campos se le añadirá, además del prefijo, un sufijo munérico empezando en 1 para la segunda posición; esto es asi para evitar cambiar el nombre de los campos de la primera posición en el caso de recibir un elemento inesperado.

Por ejemplo, si queremos explotar el campo nombre la llamada podría ser asi:

.. code-block:: python
    from datarefinery.FieldOperations import explode

    explode_name = explode("name")
    (res, err) = explode_name({"name": {"first": "Bob", "last": "Dylan"}})
    print(res) # {"name_first": "Bob", "name_last": "Dylan"}

Sustituyendo valores
....................

Cuando se estudian los datos en raras ocasiones una columna tiene todos los valores correctamente rellenos. Es muy útil el sustituir un valor cuando este cumple una condición en concreto, pero para añadir flexibilidad usaremos dos funciones, una que debe devolver true o false, y otra función que generará un nuevo valor si la primera función devuelve true; ambas funciones recibiran el valor del campo.

Por ejemplo, si queremos sustituir por cero todos los valores negativos de un campo:

.. code-block:: python
    from datarefinery.FieldOperations import replace_if

    change = replace_if(lambda x: x<0, lambda x: 0)
    (res, err) = change(-3)
    print(res) # 0

Procesando fechas y horas
.........................

Las fechas son siempre una fuente de problemas, la variedad de formatos puede ser abrumadora. Para ellos tenemos una función de intenta parsear varios formatos diferentes, y si no lo consigue informa del error para que se añada un formato nuevo.

Los formatos esperados deben ser formatos de fecha estandar de Python.

.. code-block:: python
    from datarefinery.FieldOperations import date_parser

    parser = date_parser(["%Y-%m-%d"])
    (res, err) = parser("2017-03-22")
    print(res) # <datetime class>

Hay una función similar solo para formatear horas, minutos y segundos.

Explosión temporal
..................

Tanto para fechas, como para tiempo, es posible que queramos tener los integrantes del valor como números simples en diferentes campos. Como entrada espera siempre un valor de tipo datetime.

.. code-block:: python
    import datetime
    from datarefinery.FieldOperations import explode_date

    (res, err) = explode_date(datetime(2017,3,22))
    print(res) # {"year": 2017, "month": 3, "day": 22, "hour":0, "minute": 0, "second": 0}

Si hay varias fechas en tu evento considera usar la función [add_prefix](###Prefijo de columna). SI no necesitas todos los campos de la fecha considera usar [remove column](###Quitando columnas). Esta función se usa típicamente en conjunción con un date_parser.

Quitando columnas
.................

Este método es habitualmente una fuente de confusión. Su uso en solitario no tiene sentido debido a que no puede afectar a todo el evento. Está diseñado solo para ser usado en conjunto con otras funciones de campo que generan varios campos.

En el caso de que quieras eliminar una columna, simplemente no operes sobre ella, la función ETL solo pondrá en el output los campos con los que operes.

Si este es el primer caso de composición que ves considera revisar primero la [documentación](##Combinando operaciones de campo) a este respecto.

.. code-block:: python
    import datetime
    from datarefinery.tuple.TupleDSL import compose
    from datarefinery.FieldOperations import explode_date, remove_columns

    only_year_month = compose(explode_date, remove_columns("day", "hour", "minute", "sencond"))
    (res, err) = only_year_month(datetime(2017,3,22))
    print(res) # {"year": 2017, "month": 3}

Buscando el valor
.................

Hay veces que muchos cambios en un campo son variados pero estáticos, como en asignación de coordenadas a una provincia. Para estos casos tener un diccionario de elementos donde la entrada y el valor estén representados por la clave y el valor respectivamente es una solución muy cómoda.

A la función match_dict se le pasa este diccionario contexto y se encarga de devolver el valor correspondiente de la clave con la que se llama a la función.

.. code-block:: python
    from datarefinery.FieldOperations import match_dict

    d = {"Spain": "ES", "United States of America": "US"}
    iso_decoder = match_dict(d)
    (res, err) = iso_decoder("Spain")
    print(res) # "ES"

Combinando operaciones de campo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toda la arquitectura gira en torno a este concepto, muy potente, de programación funcional que nos permite construir aplicaciones muy complejas con bloques muy sencillos de código (funciones) fáciles de probar y mantener.

La composición se parece mucho a la promación tradicional en que tenemos un conjunto sencillo de operaciones que combinados pueden resolver infinidad de situaciones.
Todas las funciones de la librería se pueden combinar para generar estos comportamientos con la función combine.

Pero este concepto se puede ver mejor con algunos ejemplos.

Normalización numérica
......................

Convertir un número de entrada en texto a un número y luego llevar a cabo una normalización min max.

.. code-block:: python
    from datarefinery.tuple.TupleDSL import compose
    from datarefinery.FieldOperations import type_enforcer, min_max_normalization

    str_2_min_max = compose(
        type_enforcer(lambda x: int(x)),
        min_max_normalization(0, 100)
    )
    (res, err) = str_2_min_max("50")
    print(res) # 0.5

Fecha completa
..............

Otra operación típica es la de explotar una fecha, querase solo con los años, meses y dias, y añadir un prefijo para evitar colisiones con otros campos.

.. code-block:: python
    from datarefinery.tuple.TupleDSL import compose
    from datarefinery.FieldOperations import date_parser, explode_date, remove_columns, add_column_prefix

    complete_date = compose(
        date_parser(["%Y-%m-%d"]),
        explode_date,
        remove_columns("hour", "minute", "second"),
        add_column_prefix("x")
    )
    (res, err) = complete_date("2017-03-22")
    print(res) # {"x_year": 2017, "x_month": 3, "x_day": 22}

One hot vector del día
......................

Incluso podemos llevar a cabo una transformación mucho más atrevida, como construir un one hot vector, desde una fecha en texto, con el día de la semana.

.. code-block:: python
    from datarefinery.tuple.TupleDSL import compose
    from datarefinery.tuple.TupleOperations import wrap
    from datarefinery.FieldOperations import date_parser, match_dict, column_category

    week_days={
        0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"
    }

    def day_of_week(dat):
      return dat.weekday()

    day_hot = compose(
        date_parser(["%Y-%m-%d"]),
        wrap(day_of_week),
        match_dict(week_days),
        column_category(week_days.values())
    )

    (res, err) = day_hot("2017-10-19")
    print(res) # {"Mo": 0, "Tu": 0, "We": 0, "Th": 1, "Fr": 0, "Sa": 0, "Su": 0}

Operaciones de evento
---------------------

Pero las funciones de campo no dicen que queremos hacer con el valor transformado; tal vez quiero que el valor se guarde en un campo con el mismo nombre; o a lo mejor quiero que tenga un nombre de campo diferente. En este nivel tenemos las funciones de fila, que funcionan de forma ligeramente diferente, ya que reciben el input, el output acumulado hasta este momento y el error acumulado hasta este momento; y se espera que devuelvan lo mismo, es decir, input, output y error.

Esto les da el control total en cada paso de la transformación de lo que está pasando, por lo que tienen una gran responsabilidad; es recomendable usar las existentes, aunque se pueden definir nuevas como veremos más adelante.

Listado de funciones
~~~~~~~~~~~~~~~~~~~~

Keep - Mantener campos
......................

La operación más sencilla, que no requiere de ninguna función de campo, es Keep. Básicamente coge un campo del input y lo pone en el output sin modificar su valor:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import keep

    operation = keep(["greet"])
    (inp, res, err) = operation({"greet": "hello", "who": "world"}, {}, {})
    print(res) # {"greet": "hello"}

Existe una versión de esta función que funciona exactamente igual pero que recibe una expresión regular como selector de campos. Se llama keep_regexp.

Substitution - Substituir campos
................................

La siguiente operación si que requiere de una función de campo. Substitution pondrá el campo, con el mismo nombre, en el output pero con el valor transformado por la función de campo que se provea. Por ejemplo, una función to_float que transforme el valor dado en un float podrían usarse así:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, substitution

    operation = substitution(["greet"], wrap(lambda x: len(x)))
    (inp, res, err) = operation({"greet": "hello", "who": "world"}, {}, {})
    print(res) # {"greet": 5}

Append - Añadir nuevos campos a partir de uno
.............................................

En muchas ocasiones queremos añadir varios campos con una sola operación, o cambiar el nombre del campo. La operación append permite hacer esto, pero requiere que la función de campo devuelva un diccionario donde el nombre del campo será extraído de la clave del diccionario y el valor del campo del valor del diccionario.Supongamos una función de campo, llamada len_cap, que dada una cadena de texto genera los campos len, con la longitud de la cadena, y cap, con la primera letra en mayúsculas.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, append

    operation = append(["greet"], wrap(lambda x: {x: "you", "y": "None"}))
    (inp, res, err) = operation({"greet": "hello", "who": "world"}, {}, {})
    print(res) # {'hello': 'you', 'y': 'None'}

Cabe destacar que, en este caso, en el output no está el campo nombre. Esto es así porque aunque se pase a la función el nombre, esta no devuelve en ningún momento el campo nombre, solo len y cap.

Fusion - Combinar campos
........................

Si nos fijamos con atención veremos que como patrón subyacente estamos llevando a cabo una operación que genera varios campos a partir de uno. Pero es posible que necesitemos la operación opuesta, es decir, a partir de varios campos el generar uno nuevo.

Esta es una de las operaciones más complejas, y se llama fusion; para ilustrar esta función vamos a cambiar el ejemplo. Dada una función de campo suma, que suma todos los valores que recibe, vamos a generar un campo total.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, fusion

    operation = fusion(["a", "b", "c"], "sum_abc", wrap(lambda x: sum(x)))
    (inp, res, err) = operation({"a": 1, "b": 2, "c": 3}, {}, {})
    print(res) # {'sum_abc': 6}

Pero fusión también puede usarse para operaciones más complejas. Supongamos que dependiendo del valor de un campo moneda queremos aplicar un tipo de cambio concreto. Para poder llevar a cabo esta operación necesitamos saber el valor concreto del campo moneda y el campo concreto con la cantidad monetaria. Para poder llevar a cabo esto, debemos saber que, la fusión entrega a la función de transformación de campo una lista, con los parámetros ordenados, exactamente en el mismo orden en el que se especificaron, en la llamada a la operación de fusión. En el ejemplo anterior llamamos a fusión con los campos ene, feb y mar; por lo que el listado que se pasará a la función contendrá los valores 5, 15 y 18.

Con este conocimiento podríamos generar una función que recupere los valores por su orden y que llame a la función de cambio de divisa existente (to_eur).

.. code-block:: python
    def to_eur_wrapped(x):
      [currency, value] = x
      return to_eur(currency, value)

Y usarla junto con fusión para crear el campo val_eur.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, fusion

    val_eur_op = fusion(["currency", "value"], "val_eur", wrap(to_eur_wrapped))
    (inp, res, err) = val_eur_op({"currency": "USD", "value": 1})
    print(res) # {"val_eur": 0.8459}

Con este mismo ejemplo se puede intuir la siguiente funcionalidad, fusion_append.

Fusion_append - Varios entran, varios salen
...........................................

Básicamente es una operación en la que usamos varios campos para generar varios campos. La función de columna recibirá la lista de campos ordenados al igual que en el caso de un fusion. Pero en esta ocasión se espera que devuelva un diccionario con los mismos parametros que en la operación de fusión.

Modificando la función del ejemplo anterior podemos devolver varios campos para no perder los datos originales en una sola operación:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, fusion_append

    def to_eur_cols(x):
      [currency, value] = x
      return {"EUR": to_eur(currency, value), currency: value}

    val_eur_op = fusion_append(["currency", "value"], "val_eur", wrap(to_eur_cols))
    (inp, res, err) = val_eur_op({"currency": "USD", "value": 1})
    print(res) # {"EUR": 0.8459, "USD": 1}

Filter_tuple - Sólo filas vip
.............................

En algunos casos estamos trabajando con un dataset del que solo queremos una parte. En este caso podemos usar la opración filter_tuple que nos permite descartar las filas que no cumplen una función concreta.

Por ejemplo, si necesitamos descartar las filas que no tengan un campo nulo; primero necesitamos una función que devuelve true si la fila no es nula. Usandola en filter_tuple quedaría algo así.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, filter_tuple

    no_none = filter_tuple(["value"], wrap(lambda x: x is not None))

    (inp, res, err) = no_none({"value": None})
    print(res) # None

Cuando la función no devuelve un output, pero tampoco un error es porque la esa fila se ha descartado.

Alternative - Plan B
....................

En muchas ocasiones una operación en concreto no se puede llevar a cabo. Pero sabemos que otra operación puede salver el día. En este caso queremos darle al ETL una operación alternativa.

Supongamos que queremos multiplicar el campo valor por dos, pero si no viene nos vale con poner un 0.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, alternative, substitution, append

    need_value = alternative(
        substitution(["value"], wrap(lambda x: x*2)),
        append(["name"], wrap(lambda x: {"value": 0}))
    )
    (inp, res, err) = need_value({"name": "John"})
    print(res) # {"value": 0}

La alternativa se usa cuando la primera opción da un error. Si da un error, por supuesto, ningún cambio que se haya llevado a cabo llegará al output.

Fallo con estilo
................

Cuando registramos el fallo, a cualquier nivel, no detenemos el proceso; si escribes tus propias funciones para la librería asegurate de que son resistentes al fallo. Esto nos permite llevar a cabo una operación especial, el recuperarnos de un error. La operación recover lee del error, escribe en el output y si todo va bien borra del error el campo relacionado. En el siguiente ejemplo, el tercer parametro es el input de error de la función y el segundo el output.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, recover

    no_error = recover(["value"], wrap(lambda x: 0))
    (inp, res, err) = no_error({},{},{"value": "not found"})
    print(res) # {"value": 0}
    print(err) # {}

Combinando operaciones de evento
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una transformación no solo se compone de un cambio. Es decir, no solo nos quedamos con un grupo de campos; o no solo sustituimos los valores de una forma concreta. Normalmente nos quedamos un campos, cambiamos el valor de otro de una forma concreta y de un tercer campo de forma completamente diferente.

A si que necesitamos un interfaz que lo permita. En este caso tenemos *Tr*. Este objeto envuelve la operación para evento y expone métodos que nos ayudan a expresar como queremos que funcionen los campos.

Especialmente destacan *then* y *apply*. Cuando llamamos a *then* este devuelve un nuevo objeto *Tr* que contiene una secuencia con las operaciones anteriores y la operación que hemos pasado a la función then.
Una vez que tenemos todas las funciones encadenadas necesitamos una función que nos permita transformar los datos, ya que en este punto tenemos un objeto *Tr*. Para esto llamamos a la función *apply*. Esta función devuelve una sola función, generada en ese momento, que engloba todas las operaciones encadenadas, y que además tiene el mismo interfaz que una operación de fila.
Ten en cuenta que en cuanto llamamos a apply perdemos las funciones *then* y *apply*.

Si por ejemplo queremos guardar un campo y sustutir el valor de otro con la función x2 (multiplica un valor por dos) podríamos escribir el siguiente código.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, keep, substitution
    from datarefinery.Tr import Tr

    x2 = wrap(lambda x: x*2)

    tr = Tr(keep(["name"])).then(substitution(["value"], x2))
    operation = tr.apply()
    (inp, res, err) = operation({"name": "John", "value": 10})
    print(res) # {"name": "John", "value": 20}

Errores comunes a evitar son pasarle los datos a apply, que no hace nada más que devolver la función a usar. O llamar a la función que estamos pasando a la operación (se pasa sin paréntesis).

.. code-block:: python
    from datarefinery.tuple.TupleOperations import substitution

    substitution(["value"], x2()) # WRONG!!!

En este caso estamos llamando a la función, mientras que en realiad la operación espera una referencia a la función y no el resultado de la llamada sin parámetros.

Esto suele pasar porque algunas de las funciones de la libería reciben parámetros (como min_max_normalization) y devuelven la referencia a la función como resultado y otras no (como explode_date) que se usa directamente la referencia.

Un bosque de posibilidades
..........................

Al usar un objeto para encapsular las transformaciones, y este objeto ser inmutable, se da el caso de que podemos guardar pasos intermedios en el proceso de transormación de datos, lo cual es especialmente útil cuando tenemos, por ejemplo, datos de entrenamiento y datos de ejecución.

Los datos de entrenamiento suelen ser como los de ejecución pero contienen un campo extra "label" que suele indicar lo que tiene que aprender (o inferir) el modelo de machine learning.

En el siguiente ejemplo la transformación de datos (el objeto Tr) se construye en un módulo especifico de tu aplicación, y se recupera con la función etl(). Luego añadiremos la lógica para el label:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import keep

    tr = etl()
    if training == True:
        tr = tr.then(keep("label"))
    operation = tr.apply()

De esta forma si estamos en la fase de entrenamiento la salida contendrá el label necesario sin tener que saber a priori cuales son las transformaciones específicas para ese set de datos.

Then - Empujando transformaciones al inicio
...........................................

En ocasiones hay datos que nos llegan en formatos que no entendemos, la librería solo maneja diccionarios de python internamente, o tal vez necesitamos hacer una operación al inicio del proceso.

El interfaz de Tr tiene una función para llevar a cabo esta operación: init. Esta pone al principio de la secuencia de transformaciones la función de evento que pongamos.

En el modulo datarefinery.tuple.Formats encontrarás varias operaciones que transforman el input de los formatos más populares a diccionarios de python. Como además esta es una función que se usa mucho para "leer" los datos el interfaz tiene una función *reader* que no es más que un alias de *init*.

Hay que tener cuidado si queremos usar init y tenemos guardadas en variables Tr intermedios que queremos diverger. Ya que todos los Tr que divergen tienen en común la misma referencia a la raiz.

**TODO: dibujo de raíz de transformaciones**

Si llevamos a cabo esta operación:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import keep
    from datarefinery.tuple.Formats import from_json

    step1 = etl()
    step2 = op1.then(keep("label"))
    final = step2.init(from_json)

En este caso tanto step1 como step2 tendrían como primera operación *from_json*, y es posible que no es esto lo que queramos llevar a cabo. Si queremos que cada una mantenga un origen independiente te sugiero que uses el siguiente código en su lugar:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import keep
    from datarefinery.tuple.Formats import from_json

    step1 = etl()
    step2 = etl().then(keep("label"))
    final = step2.init(from_json)

Peek - Cata de datos
....................

La función *peek* permite leer y manipular los datos sin miedo a modificarlos. Es especialmente útil cuando queremos guardar los datos de un paso intermedio sin parar la transformación.

Ten en cuenta que la función no se llama hasta que no se invoca la función de transformación de datos generada mediante *apply*. Además debes saber que la función se ejecuta sincronamente, es decir, hasta que la función *peek* no termina de ejecutarse el proceso no continua, pero falle o no, el proceso continuará.

Debido a que se suele llamar para escribir datos los datos en una fuente externa, el método *writer* de Tr es un alias de *peek*.

Secuencialidad
..............

Cuando se encadenan funciones con then todas ellas pasan en un solo "paso". Es decir que todas usan el mismo input y escriben en el mismo output. Por lo que si queremos modificar el valor de un campo ya modificado, aunque lo encadenemos con then, pasan a la vez y recibimos el valor de la segunda transformación solamente. Por ejemplo:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, substitution
    from datarefinery.Tr import Tr

    x2 = wrap(lambda x: x*2)

    tr = Tr(substitution("value", x2)).then(substitution("value", x2))
    operation = tr.apply()
    (inp, res, err) = operation({"value": 2})
    print(res) # {"value": 4}

Si pensamos secuencialmente esperamos que si se aplica la función x2 dos veces sobre el campo deberíamos obtener 8, pero eso no es así; al aplicarse de forma paralela lo que está pasando en realidad es algo más bien así:

| input | value (1º vez) | value(2º vez) |
| ----- | -------------- | ------------- |
| 2     | 4              | 4             |

Al pasar al mismo tiempo el input es 2 en las dos llamadas a la función. Y además el resultado de la segunda está sobreescribiendo el resultado de la primera.

Si queremos llevar a cabo estas operaciones, y obetener el resultado esperado, la solución optima es usar compose; que nos permite secuenciar las operaciones de campo, como ya hemos visto, en una sola referencia de función, que es lo que espera la función de fila. El código quedaría así:

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, substitution, compose
    from datarefinery.Tr import Tr

    x2 = wrap(lambda x: x*2)

    tr = Tr(substitution("value", compose(x2,x2)))
    operation = tr.apply()
    (inp, res, err) = operation({"value": 2})
    print(res) # {"value": 8}

Hay una otra opción para llevar a cabo esta operación. Dentro de las operaciones podemos usar change, que lleva a cabo una sustitución pero usa el valor del output en lugar del input, y **sobreescribe** el valor del output con el nuevo valor.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, substitution, change
    from datarefinery.Tr import Tr

    x2 = wrap(lambda x: x*2)

    tr = Tr(substitution("value", x2)).then(change("value", x2))
    operation = tr.apply()
    (inp, res, err) = operation({"value": 2})
    print(res) # {"value": 8}

Otra opción es el uso de [DSL](##DSL) de bajo nivel que permite configurar una operación de evento tan compleja como queramos.

En el caso de que queramos llevar cabo esta transformación, pero no tengamos acceso a la operación de campo original, podemos usar la operación de evento chain. Que termina con la operación que estamos llevando a cabo en ese momento y pasa el output al input, para que lo usen las siguientes operaciones propagando el error si es necesario, y **descarta el input** anterior.

.. code-block:: python
    from datarefinery.tuple.TupleOperations import wrap, substitution, chain
    from datarefinery.Tr import Tr

    x2 = wrap(lambda x: x*2)

    tr = Tr(substitution("value", x2)).then(chain).then(substitution("value", x2))
    operation = tr.apply()
    (inp, res, err) = operation({"value": 2})
    print(res) # {"value": 8}

Por favor, considera su uso la última opción, es una operación **muy peligrosa** ya que se **pierde el input original**. Esto significa que si te quedan operaciones que hacer con los campos originales no podrás hacerla después. Es especialmente destructivo su uso dentro de un módulo donde un usuario de tu código perdería el input irremediablemente.

DSL
~~~


El dsl de bajo nivel nos permite crear cualquier operación que se nos pueda imaginar respecto de una fila, pero como siempre todo gran poder conlleva una gran responsabilidad. Queda bajo tu responsabilidad propagar el input, el output modificado (si procede) y el error modificado (si procede).

Su uso es bastante sencillo, básicamente todas las funciones de evento se crear con este DSL, para ejemplificar su uso vamos a ver como está declarado keep:

.. code-block:: python
    def keep(fields) -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
        operations = [compose(use_input(), read_field(f), write_field(f)) for f in fields]
        return reduce(compose, map(apply_over_output, operations))

Como puedes ver es una composición donde especificamos los pasos por cada campo y finalmente reducimos de nuevo a una sola función con compose. Hay también funciones para usar el input, para usar el error... para casi todas las operaciones que se te puedan ocurrir.

En última instancia puedes generarte tu propia función de 0, aunque te recomiendo seguir la filosofía de atomizar lo máximo posible en funciones de código pequeñas; simplemente debes devolver una fucnión que reciba los tres diccionarios que representan el input, el output y el error y los retorne modificados como proceda.

Repaso con ejercicios
---------------------

Si quieres hacer algunos ejercicios para practicar, puedes ejecutar el contenedor así:

.. code-block:: bash

    docker run -it --rm -p 8888:8888 -v [tu ruta del proyecto etl-func]:/home/jovyan/work datarefinery-notebook:latest


Desde jupyter, puedes acceder al notebook con ejercicios básicos en /work/docs/notebooks/thebasics.ipynb.

