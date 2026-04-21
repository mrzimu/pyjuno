from pathlib import Path

import pytest
import uproot
import uproot_custom

import pyjuno  # noqa: F401


@pytest.fixture(scope="session")
def data_dir():
    yield Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def f_test_rec(data_dir):
    yield uproot.open(data_dir / "test_rec.root")


@pytest.fixture(scope="session")
def f_test_elec(data_dir):
    yield uproot.open(data_dir / "test_elec.root")


@pytest.fixture(scope="session")
def trees_to_test():
    yield {i.split(":")[0] for i in uproot_custom.AsCustom.target_branches}
