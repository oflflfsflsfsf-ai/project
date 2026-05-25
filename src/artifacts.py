from abc import ABC, abstractmethod
import warnings


class Artifact(ABC):
    def __init__(self):
        self.__durability = 100.0

    @abstractmethod
    def activate(self, thread) -> float: ...

    @property
    def durability(self):
        return self.__durability

    @durability.setter
    def durability(self, value):
        self.__durability = max(0.0, value)


class CrystalCore(Artifact):
    def __init__(self):
        super().__init__()

    def activate(self, thread):
        self.durability -= 2
        return round(thread.frequency * thread.stability * 1.5, 4)

    def describe(self):
        return f"CrystalCore: x1.5 резонанс, прочность={self.durability:.1f}"


class RuneMatrix(Artifact):
    def __init__(self, capacity=5):
        super().__init__()
        self.capacity = capacity
        self._stored = []

    def store(self, thread):
        if len(self._stored) < self.capacity:
            self._stored.append(thread)

    def activate(self, thread):
        self.durability -= 1
        total = thread.frequency * thread.stability
        for t in self._stored:
            total += t.frequency * t.stability
        return round(total, 4)

    def describe(self):
        return f"RuneMatrix: stored={len(self._stored)}/{self.capacity}, прочность={self.durability:.1f}"
