from pathlib import Path

import pytest

import pyjuno


@pytest.mark.parametrize(
    "tree_path",
    [
        "Event/Gen/GenHeader",
        "Event/Sim/SimHeader",
        "Event/Sim/SimEvt",
    ],
)
def test_sim(f_sim: Path, tree_path: str):
    f_sim[tree_path].arrays()
