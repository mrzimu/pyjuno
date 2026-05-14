import pyjuno


def test_rec(f_test_rec, subtests):
    event = f_test_rec["Event"]
    sub_evts = ["Sim", "CdLpmtCalib"]

    for sub_evt in sub_evts:
        sub_dir = event[sub_evt]
        with subtests.test(tree=sub_evt):
            for k in sub_dir.keys():
                sub_dir[k].arrays()


def test_elec(f_test_elec, subtests):
    event = f_test_elec["Event"]
    sub_evts = [
        "Sim",
        "CdLpmtTruth",
        "CdSpmtTruth",
        "TrackTruth",
        "CdSpmtElec",
        "CdWaveform",
        "CdTrigger",
    ]

    for sub_evt in sub_evts:
        sub_dir = event[sub_evt]
        with subtests.test(tree=sub_evt):
            for k in sub_dir.keys():
                sub_dir[k].arrays()


def test_metadata(f_test_rec):
    f_test_rec["Meta/navigator"].arrays()
    f_test_rec["Meta/FileMetaData"].all_members
    f_test_rec["Meta/UniqueIDTable"].all_members


def test_assemble_event_elec(f_test_elec):
    arr1 = pyjuno.assemble_event(f_test_elec, entry_stop=10, filter_path="*pmtTruth")
    assert len(arr1.fields) == 2

    arr2 = pyjuno.assemble_event(
        f_test_elec,
        entry_stop=10,
        filter_path=["*CdLpmtTruth", "*CdSpmtTruth", "*TrackTruth"],
    )
    assert len(arr2.fields) == 3
