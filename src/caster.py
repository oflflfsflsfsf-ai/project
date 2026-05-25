import warnings
import logging
from typing import Protocol, runtime_checkable

logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@runtime_checkable
class ArcaneInterface(Protocol):
    def cast(self, caster, target: str) -> str: ...
    def describe(self) -> str: ...


class Caster:
    def __init__(self, name, energy, artifact=None):
        self.name = name
        self.energy = energy
        self.artifact = None
        self.__spell_book = []
        if artifact:
            self.equip(artifact)

    def equip(self, artifact):
        if self.artifact is not None:
            warnings.warn(f"{self.name}: артефакт уже экипирован, заменяю", UserWarning)
        self.artifact = artifact

    def learn(self, spell):
        self.__spell_book.append(spell)

    def forget(self,spell_name):
        self.__spell_book = [s for s in self.__spell_book if s.name != spell_name]

    def cast(self, spell_name, target):
        for spell in self.__spell_book:
            if spell.name == spell_name:
                try:
                    return spell.cast(self, target)
                except Exception as e:
                    logger.error(f"Ошибка каста '{spell_name}': {e}")
                    raise
        raise ValueError(f"Заклинание '{spell_name}' не найдено")

    def __len__(self):
        return len(self.__spell_book)

    def __str__(self):
        return f"[Нитяр {self.name} | energy={self.energy:.1f} | заклинаний={len(self)}]"

    def __repr__(self):
        return f"Caster(name={self.name!r}, energy={self.energy}, spells={len(self)})"


def execute_all(spells, caster, target):
    for spell in spells:
        print(spell.cast(caster, target))
