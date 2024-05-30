from typing import List, Callable
from abc import ABC, abstractmethod

# Define the Observer interface. This class is an example that could be inherited,

# alternatively define your own call function in the Observable class, such as in InteractivePlot


class Observer(ABC):
    """
    Abstract base class for defining the Observer in the Observer pattern.

    The Observer pattern is a software design pattern in which an object,
    called the subject, maintains a list of its dependents, called observers,
    and notifies them automatically of any state changes, usually by calling
    one of their methods.

    This class uses the `ABC` module from Python's standard library to create
    an abstract base class. An abstract base class is a base class that cannot
    be instantiated and defines methods that must be implemented by its
    subclasses. This ensures a consistent interface for all observers.

    The `abstractmethod` decorator is used to declare methods that have to be
    overridden by concrete subclasses. This enforces the implementation of
    these methods in each subclass, ensuring that they adhere to the defined
    interface.
    """

    @abstractmethod
    def call(self, event: str, *args, **kwargs):
        """
        Abstract method that must be implemented by concrete subclasses.

        This method is called when the subject (Observable) to which the
        observer is attached, triggers an event. The subclass should implement
        the logic for handling these events here.

        Parameters:
        event (str): The name of the event that has been triggered.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
        """
        pass


# Define the Observable (Subject) interface
class Observable:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, event: str, *args, **kwargs):
        for observer in self._observers:
            observer.call(event, *args, **kwargs)
