import awkward.contents
import awkward.forms
import awkward.index
from uproot_custom import AsCustom, Factory, GroupFactory, build_factory, registered_factories

from pyjuno.pyjuno_cpp import AnyJMClassReader, JMSmartRefReader

AsCustom.target_branches |= {
    "/Event/Gen/GenHeader:GenHeader/m_event",
    # GenEvt is not supported.
    "/Event/Sim/SimHeader:SimHeader/m_event",
    "/Event/Sim/SimEvt:SimEvt/m_tracks",
    "/Event/Sim/SimEvt:SimEvt/m_vertices",
    "/Event/Sim/SimEvt:SimEvt/m_cd_hits",
    "/Event/Sim/SimEvt:SimEvt/m_wp_hits",
    "/Event/Sim/SimEvt:SimEvt/m_tt_hits",
    "/Event/WpCalib/WpCalibHeader:WpCalibHeader/m_event",
    "/Event/WpCalib/WpCalibEvt:WpCalibEvt/m_calibPMTCol",
    "/Event/CdLpmtCalib/CdLpmtCalibHeader:CdLpmtCalibHeader/m_event",
    "/Event/CdLpmtCalib/CdLpmtCalibEvt:CdLpmtCalibEvt/m_calibPMTCol",
    "/Event/CdSpmtCalib/CdSpmtCalibHeader:CdSpmtCalibHeader/m_event",
    "/Event/CdSpmtCalib/CdSpmtCalibEvt:CdSpmtCalibEvt/m_calibPMTCol",
    "/Event/CdVertexRec/CdVertexRecHeader:CdVertexRecHeader/m_event",
    "/Event/CdVertexRec/CdVertexRecEvt:CdVertexRecEvt/m_vertices",
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

        if top_type_name == "JM::SmartRef":
            return None

        sub_streamers: list = all_streamer_info[top_type_name]
        sub_factories = [build_factory(s, all_streamer_info, item_path) for s in sub_streamers]
        return cls(name=top_type_name, sub_factories=sub_factories)

    def build_cpp_reader(self):
        sub_readers = [s.build_cpp_reader() for s in self.sub_factories]
        return AnyJMClassReader(self.name, sub_readers)


registered_factories.add(JMSmartRefFactory)
registered_factories.add(AnyJMClassFactory)
