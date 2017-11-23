Tuple DSL documentation
=======================

DSL
~~~

DSL let us create any operation over a row, but you know... with great power comes great responsibility_.
::_responsibility: https://i.annihil.us/u/prod/marvel//universe3zx/images/4/4f/Ben_parker.jpg

When you create an operation, you have to spread the input, the modified output and the error if proceeds.

Its usage is very simple. For example, *keep* function is shown below:

.. code-block:: python

    def keep(fields) -> Callable[[dict, dict, dict], Tuple[dict, dict, dict]]:
        operations = [compose(use_input(), read_field(f), write_field(f)) for f in fields]
        return reduce(compose, map(apply_over_output, operations))

In this example you can see a composition that takes different functions for every field. *keep* returns an unique function
that contains all of them applied on output.

List of functions
-----------------

- use_input
- use_output
- read_field
- read_match
- read_fields
- write_field
- write_error_field
- dict_enforcer
- apply_over_output
- compose

You can create your own function too. It has to return a function that takes 3 dictionaries (input, output and error)
and returns them modified if it's necessary.
