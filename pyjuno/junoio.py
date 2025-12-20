import awkward.contents
import awkward.forms
import awkward.index
from uproot_custom import AsCustom, Factory, GroupFactory, build_factory, registered_factories
from uproot_custom.factories import ObjectHeaderFactory
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


registered_factories.add(JMSmartRefFactory)
registered_factories.add(AnyJMClassFactory)
registered_factories.add(AnyCLHEPClassFactory)
