from collections import defaultdict


class Updateable(type):
    _instances = defaultdict(list)

    def __new__(mcs, cls_name, bases, namespace):
        cls_instance = super().__new__(mcs, cls_name, bases, namespace)
        methods = mcs._get_methods(namespace)

        for instance in mcs._instances[cls_name]:
            for method_name, func in methods.items():
                setattr(instance, method_name, func)

        mcs._instances[cls_name].append(cls_instance)

        return cls_instance

    @staticmethod
    def _get_methods(namespace):
        return {name: value for name, value in namespace.items() if callable(value)}