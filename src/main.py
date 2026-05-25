from threads import Thread, EnergyThread, FormThread, TimeThread
from spells import WeaveSpell, CutSpell, BindSpell, LegendaryWeaveSpell, CombinedSpell, Rarity
from artifacts import CrystalCore, RuneMatrix
from caster import Caster, execute_all

# --- Создаём нитяров ---
varn = Caster("Архимаг Варн", energy=200)
sel  = Caster("Ученица Сел", energy=40)

# --- Нити каждого типа ---
e_thread = EnergyThread(100.0, 0.9, "Огонь", power=1.2)
f_thread = FormThread(50.0, 0.8, "Кристалл", shape="cube")
t_thread = TimeThread(200.0, 0.7, "Эпоха", era=3)
print("Перегрузка +:", e_thread + f_thread)

# --- Экипируем артефакты ---
varn.equip(RuneMatrix(capacity=3))
sel.equip(CrystalCore())

# Попытка заменить артефакт → предупреждение
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    sel.equip(CrystalCore())
    if w:
        print("Предупреждение:", w[0].message)

# --- Заклинания ---
weave   = WeaveSpell("ThreadWeave", cost=10)
cut     = CutSpell("SilverCut", cost=15, severity=0.2)
bind    = BindSpell("EternalBind", cost=20, duration=5)
leg     = LegendaryWeaveSpell("OmegaWeave", cost=30, bonus=2.0)
combo   = CombinedSpell("FullCombo", [weave, cut])

for spell in [weave, cut, bind, leg]:
    varn.learn(spell)
sel.learn(combo)

# --- Дуэль ---
print("\n=== ДУЭЛЬ ===")
for spell in [weave, cut, bind, leg]:
    print(spell.cast(varn, sel.name))

print("\n--- Сел атакует Варна ---")
print(combo.cast(sel, varn.name))

# --- Duck typing ---
print("\n=== execute_all (duck typing) ===")
mixed = [weave, cut, leg, combo]
execute_all(mixed, varn, "цель")

# --- Итоговый отчёт ---
print("\n=== ИТОГ ===")
print(varn)
print(sel)
print(f"Заклинаний у Варна: {len(varn)}")
print(f"Артефакт Варна: {varn.artifact}")
print(f"Артефакт Сел: {sel.artifact}")

# --- Полиморфизм > ---
print("\nleg > weave:", leg > weave)

# --- MRO ---
print("\nMRO LegendaryWeaveSpell:")
for c in LegendaryWeaveSpell.__mro__:
    print(" ", c)
