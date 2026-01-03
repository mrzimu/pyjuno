import awkward as ak
import awkward.contents
import awkward.forms
import awkward.index
import numpy as np
import uproot.model
import uproot_custom.cpp
from uproot_custom import (
    AsCustom,
    Factory,
    GroupFactory,
    ObjectHeaderFactory,
    build_factory,
    registered_factories,
)

from pyjuno.pyjuno_cpp import AnyCLHEPClassReader, AnyJMClassReader, JMSmartRefReader

AsCustom.target_branches |= {
    # Meta
    "/Meta/navigator:EvtNavigator/m_refs",
    # Gen
    "/Event/Gen/GenHeader:GenHeader/m_event",
    # Sim
    "/Event/Sim/SimHeader:SimHeader/m_event",
    "/Event/Sim/SimEvt:SimEvt/m_tracks",
    "/Event/Sim/SimEvt:SimEvt/m_vertices",
    "/Event/Sim/SimEvt:SimEvt/m_cd_hits",
    "/Event/Sim/SimEvt:SimEvt/m_wp_hits",
    "/Event/Sim/SimEvt:SimEvt/m_tt_hits",
    # WpCalib
    "/Event/WpCalib/WpCalibHeader:WpCalibHeader/m_event",
    "/Event/WpCalib/WpCalibEvt:WpCalibEvt/m_calibPMTCol",
    # CdLpmtCalib
    "/Event/CdLpmtCalib/CdLpmtCalibHeader:CdLpmtCalibHeader/m_event",
    "/Event/CdLpmtCalib/CdLpmtCalibEvt:CdLpmtCalibEvt/m_calibPMTCol",
    # CdSpmtCalib
    "/Event/CdSpmtCalib/CdSpmtCalibHeader:CdSpmtCalibHeader/m_event",
    "/Event/CdSpmtCalib/CdSpmtCalibEvt:CdSpmtCalibEvt/m_calibPMTCol",
    # CdLpmtTruth
    "/Event/CdLpmtTruth/CdLpmtElecTruthHeader:CdLpmtElecTruthHeader/m_event",
    "/Event/CdLpmtTruth/CdLpmtElecTruthEvt:CdLpmtElecTruthEvt/m_truths",
    # CdSpmtTruth
    "/Event/CdSpmtTruth/CdSpmtElecTruthHeader:CdSpmtElecTruthHeader/m_event",
    "/Event/CdSpmtTruth/CdSpmtElecTruthEvt:CdSpmtElecTruthEvt/m_truths",
    # TrackTruth
    "/Event/TrackTruth/TrackElecTruthHeader:TrackElecTruthHeader/m_event",
    "/Event/TrackTruth/TrackElecTruthEvt:TrackElecTruthEvt/m_truths",
    # CdSpmtElec
    "/Event/CdSpmtElec/CdSpmtElecHeader:CdSpmtElecHeader/m_event",
    "/Event/CdSpmtElec/CdSpmtElecEvt:CdSpmtElecEvt/m_SpmtBlocks",
    "/Event/CdSpmtElec/CdSpmtElecEvt:CdSpmtElecEvt/m_SpmtSpecialWords",
    "/Event/CdSpmtElec/CdSpmtElecEvt:CdSpmtElecEvt/m_channelData",
    # CdTrigger
    "/Event/CdTrigger/CdTriggerHeader:CdTriggerHeader/m_event",
    # CdVertexRec
    "/Event/CdVertexRec/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRec/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # CdVertexRecJVertex
    "/Event/CdVertexRecJVertex/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRecJVertex/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # CdVertexRecMixedPhase
    "/Event/CdVertexRecMixedPhase/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRecMixedPhase/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # Muon
    "/Event/Muon/MuonHeader:MuonHeader/m_event",
    # Flasher
    "/Event/Flasher/FlasherHeader:FlasherHeader/m_event",
    # Oec
    "/Event/Oec/OecHeader:OecHeader/m_event",
    # AfterPulse
    "/Event/AfterPulse/APHeader:APHeader/m_event",
    # WpRec
    "/Event/WpRec/WpRecHeader:WpRecHeader/m_event",
    "/Event/WpRec/WpRecEvt:WpRecEvt/m_tracks",
    # WpTrigger
    "/Event/WpTrigger/WpTriggerHeader:WpTriggerHeader/m_event",
    # CdVertexRecOMILREC
    "/Event/CdVertexRecOMILREC/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRecOMILREC/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # CdVertexRecOMILREC_JVtx
    "/Event/CdVertexRecOMILREC_JVtx/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRecOMILREC_JVtx/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # CdVertexRecOMILREC_MPV
    "/Event/CdVertexRecOMILREC_MPV/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRecOMILREC_MPV/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
    # CdTrackRecClassify
    "/Event/CdTrackRecClassify/CdTrackRecHeader:CdTrackRecHeader/m_event",
    "/Event/CdTrackRecClassify/CdTrackRecEvt:CdTrackRecEvt/m_tracks",
}


class JMSmartRefFactory(Factory):
    """
    Factory for JM::SmartRef objects.
    """

    @classmethod
    def priority(cls) -> int:
        """
        Return the call priority of this factory. Factories with higher
        priority will be called first.
        """
        return 50

    @classmethod
    def build_factory(
        cls,
        top_type_name,
        cur_streamer_info,
        all_streamer_info,
        item_path,
        **kwargs,
    ):
        if top_type_name != "JM::SmartRef":
            return None

        if item_path == "/Meta/navigator:EvtNavigator/m_refs.m_refs":
            return ObjectHeaderFactory(
                name=cur_streamer_info["fName"],
                element_factory=cls(name=cur_streamer_info["fName"]),
            )

        return cls(name=cur_streamer_info["fName"])

    def build_cpp_reader(self):
        return JMSmartRefReader(self.name)

    def make_awkward_content(self, raw_data):
        arr_pidf, arr_entry = raw_data
        return awkward.contents.RecordArray(
            [
                awkward.contents.NumpyArray(arr_pidf),
                awkward.contents.NumpyArray(arr_entry),
            ],
            ["pidf", "entry"],
        )

    def make_awkward_form(self):
        return awkward.forms.RecordForm(
            [
                awkward.forms.NumpyForm("uint16"),
                awkward.forms.NumpyForm("int64"),
            ],
            ["pidf", "entry"],
        )


class AnyJMClassFactory(GroupFactory):
    class_exceptions = {
        "JM::EventObject",
        "JM::TrackElecTruth",
        "JM::SmartRef",
        "JM::FileMetaData",
        "JM::UniqueIDTable",
    }

    @classmethod
    def build_factory(
        cls,
        top_type_name,
        cur_streamer_info,
        all_streamer_info,
        item_path,
        **kwargs,
    ):
        if not top_type_name.startswith("JM::"):
            return None

        if top_type_name in cls.class_exceptions:
            return None

        sub_streamers: list = all_streamer_info[top_type_name]
        sub_factories = [build_factory(s, all_streamer_info, item_path) for s in sub_streamers]
        return cls(name=cur_streamer_info["fName"], sub_factories=sub_factories)

    def build_cpp_reader(self):
        sub_readers = [s.build_cpp_reader() for s in self.sub_factories]
        return AnyJMClassReader(self.name, sub_readers)


class AnyCLHEPClassFactory(GroupFactory):
    @classmethod
    def build_factory(
        cls,
        top_type_name,
        cur_streamer_info,
        all_streamer_info,
        item_path,
        **kwargs,
    ):
        if not top_type_name.startswith("CLHEP::"):
            return None

        sub_streamers: list = all_streamer_info[top_type_name]
        sub_factories = [build_factory(s, all_streamer_info, item_path) for s in sub_streamers]
        return cls(name=cur_streamer_info["fName"], sub_factories=sub_factories)

    def build_cpp_reader(self):
        sub_readers = [s.build_cpp_reader() for s in self.sub_factories]
        return AnyCLHEPClassReader(self.name, sub_readers)


class Model_JM_3a3a_FileMetaData(uproot.model.Model):
    def read_members(self, chunk, cursor, context, file):
        all_streamer_info: dict[str, list[dict]] = {}
        for k, v in file.streamers.items():
            cur_infos = [i.all_members for i in next(iter(v.values())).member("fElements")]
            all_streamer_info[k] = cur_infos

        s = file.streamers["JM::FileMetaData"][1]
        cls_streamer_info = {
            "fName": s.typename,
            "fTypeName": s.typename,
        }

        fac = build_factory(cls_streamer_info, all_streamer_info)
        reader = fac.build_cpp_reader()
        raw_data = uproot_custom.cpp.read_data(
            chunk.raw_data,
            np.array([0, len(chunk.raw_data)], dtype=np.int64),
            reader,
        )
        out = ak.Array(fac.make_awkward_content(raw_data))[0].tolist()
        self._members = out
        cursor.skip(len(chunk.raw_data) - cursor.index)


class Model_JM_3a3a_UniqueIDTable(uproot.model.Model):
    def read_members(self, chunk, cursor, context, file):
        all_streamer_info: dict[str, list[dict]] = {}
        for k, v in file.streamers.items():
            cur_infos = [i.all_members for i in next(iter(v.values())).member("fElements")]
            all_streamer_info[k] = cur_infos

        s = file.streamers["JM::UniqueIDTable"][1]
        cls_streamer_info = {
            "fName": s.typename,
            "fTypeName": s.typename,
        }

        fac = build_factory(cls_streamer_info, all_streamer_info)
        reader = fac.build_cpp_reader()
        raw_data = uproot_custom.cpp.read_data(
            chunk.raw_data,
            np.array([0, len(chunk.raw_data)], dtype=np.int64),
            reader,
        )
        out = ak.Array(fac.make_awkward_content(raw_data))[0]

        res = {}
        for row in out["m_tables"]:
            key = row["key"]
            val = row["val"]
            tmp_res = {}
            for sub_key in val.fields:
                tmp_res[sub_key] = val[sub_key]
            res[key] = tmp_res

        self._members = {"m_tables": res}
        cursor.skip(len(chunk.raw_data) - cursor.index)


registered_factories.add(JMSmartRefFactory)
registered_factories.add(AnyJMClassFactory)
registered_factories.add(AnyCLHEPClassFactory)
uproot.classes["JM::FileMetaData"] = Model_JM_3a3a_FileMetaData
uproot.classes["JM::UniqueIDTable"] = Model_JM_3a3a_UniqueIDTable
