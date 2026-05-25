import logging

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Thread:
    def __init__(self, frequency: float, stability: float, name: str):
        self.frequency = frequency
        self.stability = stability
        self.__name = name

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        if not (0.1 <= value <= 999.9):
            msg = f"frequency={value} вне диапазона [0.1, 999.9]"
            logging.error(msg)
            raise ValueError(msg)
        self.__frequency = value

    @property
    def stability(self):
        return self.__stability

    @stability.setter
    def stability(self, value):
        if not (0.0 <= value <= 1.0):
            msg = f"stability={value} вне диапазона [0.0, 1.0]"
            logging.error(msg)
            raise ValueError(msg)
        self.__stability = value

    @property
    def name(self):
        return self.__name

    def resonate(self, other: "Thread") -> float:
        return round((self.frequency + other.frequency) * (self.stability + other.stability) / 2, 4)

    def __add__(self, other: "Thread") -> "Thread":
        new_freq = min((self.__frequency + other.frequency) / 2, 999.9)
        new_stab = min((self.__stability + other.stability) / 2, 1.0)
        return Thread(new_freq, new_stab, f"{self.__name}+{other.name}")

    def __repr__(self):
        return f"Thread(name={self.name!r}, frequency={self.frequency}, stability={self.__stability})"

    def __str__(self):
        return f"[Нить '{self.name}' | freq={self.frequency} | stab={self.__stability}]"


class EnergyThread(Thread):
    def __init__(self, frequency, stability, name, power=1.0):
        super().__init__(frequency, stability, name)
        self.power = power

    def resonate(self, other):
        return round(super().resonate(other) * self.power, 4)


class FormThread(Thread):
    def __init__(self, frequency, stability, name, shape="sphere"):
        super().__init__(frequency, stability, name)
        self.shape = shape

    def resonate(self, other):
        return round(super().resonate(other) + self.stability * 10, 4)


class TimeThread(Thread):
    def __init__(self, frequency, stability, name, era=1):
        super().__init__(frequency, stability, name)
        self.era = era

    def resonate(self, other):
        return round(super().resonate(other) * self.era, 4)
