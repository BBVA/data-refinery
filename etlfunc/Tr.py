import copy


def _no_affect(f):
    def _app(i, o, e):
        f(copy.deepcopy(i),
          copy.deepcopy(o),
          copy.deepcopy(e)
          )
        return i, o, e
    return _app


class Tr:
    """
    expected behaviour:

    Funct

    I       |--> I'
    |       |
    O -> F -|--> O'
    |       |
    E       |--> E'

    """
    def __init__(self, func, next_tr=None):
        self.func = func
        self.next_tr = next_tr

    def then(self, func):
        return Tr(func, next_tr=self)

    def reader(self, func):
        return self.init(func)

    def init(self, func):
        if self.next_tr is not None:
            self.next_tr.init(func)
        else:
            self.next_tr = Tr(func)
        return self

    def writer(self, func):
        return self.peek(func)

    def peek(self, func):
        return Tr(_no_affect(func), next_tr=self)

    def apply(self):
        operation = None
        if self.next_tr is not None:
            operation = self.next_tr.apply()

        def _app(i, o={}, e={}):
            if operation is not None:
                (ip, op, ep) = operation(i, o, e)
            else:
                (ip, op, ep) = (i, o, e)
            if ip is None:
                return None, op, ep
            if op is None:
                return ip, None, ep
            if self.func is None:
                return ip, op, ep
            elif self.func is not None:
                return self.func(ip, op, ep)
        return _app
