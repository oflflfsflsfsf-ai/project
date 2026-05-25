from abc import ABC, abstractmethod
from enum import Enum


class Rarity(Enum):
    COMMON = "COMMON"
    RARE = "RARE"
    LEGENDARY = "LEGENDARY"


class Spell(ABC):
    def __init__(self, name, cost, rarity=Rarity.COMMON):
        self.name = name
        self.cost = cost
        self.rarity = rarity

    @abstractmethod
    def cast(self, caster, target: str) -> str: ...

    @abstractmethod
    def describe(self) -> str: ...

    def __str__(self):
        return f"[{self.rarity.value}] {self.name} (cost={self.cost})"

    def __gt__(self, other):
        order = {Rarity.COMMON: 0, Rarity.RARE: 1, Rarity.LEGENDARY: 2}
        return order[self.rarity] > order[other.rarity]


class WeaveSpell(Spell):
    def __init__(self, name, cost, rarity=Rarity.COMMON):
        super().__init__(name, cost, rarity)

    def cast(self, caster, target):
        caster.energy -= self.cost
        return f"{caster.name} сплетает нить к '{target}' [{self.name}] — энергия: {caster.energy:.1f}"

    def describe(self):
        return f"WeaveSpell '{self.name}': создаёт связь, стоимость {self.cost}"


class CutSpell(Spell):
    def __init__(self, name, cost, severity=0.1, rarity=Rarity.COMMON):
        super().__init__(name, cost, rarity)
        self.severity = severity

    def cast(self, caster, target):
        caster.energy -= self.cost
        return f"{caster.name} разрезает '{target}' [{self.name}] — стабильность -{self.severity}, энергия: {caster.energy:.1f}"

    def describe(self):
        return f"CutSpell '{self.name}': снижает стабильность на {self.severity}"


class BindSpell(Spell):
    def __init__(self, name, cost, duration=3, rarity=Rarity.COMMON):
        super().__init__(name, cost, rarity)
        self.duration = duration

    def cast(self, caster, target):
        caster.energy -= self.cost
        return f"{caster.name} связывает '{target}' [{self.name}] на {self.duration} ходов, энергия: {caster.energy:.1f}"

    def describe(self):
        return f"BindSpell '{self.name}': эффект {self.duration} ходов"


class LegendaryWeaveSpell(WeaveSpell):
    def __init__(self, name, cost, bonus=1.5):
        super().__init__(name, cost, rarity=Rarity.LEGENDARY)
        self.bonus = bonus

    def cast(self, caster, target):
        return super().cast(caster, target) + f" [ЛЕГЕНДАРНЫЙ бонус x{self.bonus}!]"

    def describe(self):
        return f"LegendaryWeaveSpell '{self.name}': усиленный WeaveSpell x{self.bonus}"


class CombinedSpell(Spell):
    def __init__(self, name, spells):
        super().__init__(name, sum(s.cost for s in spells), Rarity.RARE)
        self._spells = spells

    def cast(self, caster, target):
        return "\n".join(s.cast(caster, target) for s in self._spells)

    def describe(self):
        return f"CombinedSpell '{self.name}': {[s.name for s in self._spells]}"
