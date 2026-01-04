import os

import pytest
import uproot

import pyjuno


def test_sim(f_sim, trees_to_test: set[str], subtests):
    for tree_path in trees_to_test:
        if tree_path not in f_sim:
            continue
        with subtests.test(tree=tree_path):
            f_sim[tree_path].arrays()


@pytest.mark.skipif(
    os.getenv("PYJUNODATA") is None,
    reason="PYJUNODATA environment variable not set",
)
@pytest.mark.parametrize(
    "fpath",
    [
        "det.root",
        "rec.root",
        "miniesd.root",
        "run.root",
    ],
)
def test_self_hosted_files(fpath, trees_to_test: set[str], subtests):
    f = uproot.open(os.getenv("PYJUNODATA") + "/" + fpath)
    for tree_name in trees_to_test:
        if tree_name not in f:
            continue

        with subtests.test(tree=tree_name):
            f[tree_name].arrays(entry_stop=10)


def test_metadata(f_sim):
    f_sim["Meta/navigator"].arrays()
    f_sim["Meta/FileMetaData"].all_members
    f_sim["Meta/UniqueIDTable"].all_members


def test_assemble_event(f_sim):
    with pytest.warns(UserWarning):
        pyjuno.assemble_event(f_sim)
        pyjuno.assemble_event(f_sim, entry_start=5)
        pyjuno.assemble_event(f_sim, entry_stop=10)
        pyjuno.assemble_event(f_sim, entry_start=5, entry_stop=10)
