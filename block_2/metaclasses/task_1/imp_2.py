from typing import Any


class Updateable(type):

    """Копит у себя все ссылки на экземпляры созданных классов и
    обновляет их атибуты и методы, если они переопределяются
    в реализациях новых экземплярах."""

    instances_of_meta = []

    def __new__(metacls, cls, bases, clsdict):
        """отвечает за фактическое создание/модификацию окончательного класса"""

        def func(attr):
            def method():
                return clsdict[attr](cls)
            return method

        for instance in metacls.instances_of_meta:
            for attr in instance.__dir__():
                if attr in clsdict and not attr.startswith('__'):
                    if attr in clsdict and callable(getattr(instance, attr)):
                        setattr(instance, attr, func(attr))
                    else:
                        setattr(instance, attr, clsdict[attr])

        return super().__new__(metacls, cls, bases, clsdict)

    def __call__(metacls) -> Any:
        """вызывается, когда экземпляр класса используется как вызываемый"""

        instance = super(Updateable, metacls).__call__()
        metacls.instances_of_meta.append(instance)
        return instance

