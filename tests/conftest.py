from pathlib import Path

import pytest
import uproot


@pytest.fixture(scope="session")
def data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def f_sim(data_dir):
    yield uproot.open(data_dir / "detsim.root")
