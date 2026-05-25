import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import logging
from unittest.mock import patch, MagicMock

from threads import Thread, EnergyThread
from spells import WeaveSpell, CutSpell, LegendaryWeaveSpell, Rarity
from artifacts import CrystalCore
from caster import Caster, execute_all

# ===== Thread =====

def test_thread_valid():
    t = Thread(100.0, 0.5, "Test")
    assert t.frequency == 999
    assert t.stability == 0.5

def test_thread_invalid_frequency():
    with pytest.raises(ValueError):
        Thread(0.0, 0.5, "Bad")

def test_thread_invalid_stability():
    with pytest.raises(ValueError):
        Thread(10.0, 1.5, "Bad")

def test_thread_boundary_min():
    t = Thread(0.1, 0.0, "Min")
    assert t.frequency == 0.1

def test_thread_boundary_max():
    t = Thread(999.9, 1.0, "Max")
    assert t.stability == 1.0

def test_thread_resonate():
    a = Thread(100.0, 0.5, "A")
    b = Thread(100.0, 0.5, "B")
    assert a.resonate(b) == round(200 * 1.0 / 2, 4)

def test_thread_add():
    a = Thread(100.0, 0.6, "A")
    b = Thread(200.0, 0.8, "B")
    c = a + b
    assert c.frequency == 150.0
    assert c.stability == 0.7

# ===== Spells =====

def test_weave_spell_reduces_energy():
    caster = Caster("Mage", 100)
    spell = WeaveSpell("W", cost=10)
    spell.cast(caster, "target")
    assert caster.energy == 90

def test_legendary_gt_common():
    leg = LegendaryWeaveSpell("L", 30)
    common = WeaveSpell("C", 5)
    assert leg > common

def test_cut_spell_describe():
    s = CutSpell("Cut", 5, 0.3)
    assert "0.3" in s.describe()

# ===== Caster =====

def test_caster_learn_and_len():
    c = Caster("Hero", 100)
    c.learn(WeaveSpell("W", 5))
    assert len(c) == 1

def test_caster_forget():
    c = Caster("Hero", 100)
    c.learn(WeaveSpell("W", 5))
    c.forget("W")
    assert len(c) == 0

def test_caster_cast_not_found():
    c = Caster("Hero", 100)
    with pytest.raises(ValueError):
        c.cast("Unknown", "target")

# ===== Artifacts =====

def test_crystal_core_reduces_durability():
    t = Thread(100.0, 0.5, "T")
    a = CrystalCore()
    a.activate(t)
    assert a.durability == 98.0

# ===== Mock =====

def test_with_mock():
    with patch('artifacts.CrystalCore.activate') as mock_activate:
        mock_activate.return_value = 99.9
        core = CrystalCore()
        t = Thread(10.0, 0.5, "T")
        result = core.activate(t)
        assert result == 99.9
        mock_activate.assert_called_once()

def test_magic_mock_called_with_args():
    mock_spell = MagicMock()
    mock_spell.cast.return_value = "ok"
    caster = Caster("X", 50)
    mock_spell.cast(caster, "enemy")
    mock_spell.cast.assert_called_once_with(caster, "enemy")

def test_side_effect_exception():
    mock_spell = MagicMock()
    mock_spell.cast.side_effect = RuntimeError("внешний сбой")
    caster = Caster("X", 50)
    with pytest.raises(RuntimeError):
        mock_spell.cast(caster, "enemy")

# ===== Logging =====

def test_logging_on_invalid_frequency(tmp_path):
    log_file = tmp_path / "test.log"
    handler = logging.FileHandler(str(log_file))
    logging.getLogger().addHandler(handler)
    with pytest.raises(ValueError):
        Thread(0.0, 0.5, "Bad")
        # ===== Дополнительные тесты для покрытия =====

from spells import BindSpell, CombinedSpell, Rarity
from artifacts import RuneMatrix
from threads import FormThread, TimeThread

def test_bind_spell_cast():
    caster = Caster("Hero", 100)
    spell = BindSpell("B", cost=5, duration=3)
    result = spell.cast(caster, "target")
    assert "3 ходов" in result

def test_combined_spell_cast():
    caster = Caster("Hero", 100)
    combo = CombinedSpell("Combo", [WeaveSpell("W", 5), CutSpell("C", 5)])
    result = combo.cast(caster, "target")
    assert "Hero" in result

def test_rune_matrix_store_and_activate():
    from threads import Thread
    t1 = Thread(100.0, 0.5, "T1")
    t2 = Thread(50.0, 0.8, "T2")
    r = RuneMatrix(capacity=3)
    r.store(t1)
    result = r.activate(t2)
    assert result > 0
    assert r.durability == 99.0

def test_crystal_core_activate():
    from threads import Thread
    t = Thread(100.0, 0.8, "T")
    c = CrystalCore()
    result = c.activate(t)
    assert result == round(100.0 * 0.8 * 1.5, 4)

def test_caster_equip_warning():
    import warnings
    from artifacts import CrystalCore
    c = Caster("Hero", 100)
    c.equip(CrystalCore())
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        c.equip(CrystalCore())
        assert len(w) == 1

def test_form_thread_resonate():
    t1 = FormThread(100.0, 0.5, "F")
    t2 = FormThread(100.0, 0.5, "F2")
    result = t1.resonate(t2)
    assert result > 0

def test_time_thread_resonate():
    t1 = TimeThread(100.0, 0.5, "T", era=2)
    t2 = TimeThread(100.0, 0.5, "T2", era=2)
    result = t1.resonate(t2)
    assert result > 0

def test_legendary_weave_cast():
    caster = Caster("Hero", 100)
    spell = LegendaryWeaveSpell("L", 10, bonus=2.0)
    result = spell.cast(caster, "target")
    assert "ЛЕГЕНДАРНЫЙ" in result

def test_caster_str():
    c = Caster("Hero", 100)
    assert "Hero" in str(c)

def test_thread_str():
    from threads import Thread
    t = Thread(100.0, 0.5, "T")
    assert "Нить" in str(t)
