from abc import ABC, abstractmethod

class Entity(ABC):
    provider = None
    provided_value = None
    resolved_value = None


class DateTime(Entity):
    pass

class Date(DateTime):
    pass

class Time(DateTime):
    pass

