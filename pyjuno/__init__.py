from uproot_custom import Factory, registered_factories
import awkward as ak
import awkward.contents
import awkward.index
import awkward.forms
from pyjuno.pyjuno_cpp import JMSmartRefReader


class JMSmartRefFactory(Factory):
    """
    Factory for JM::SmartRef objects.
    """

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


registered_factories.add(JMSmartRefFactory)
