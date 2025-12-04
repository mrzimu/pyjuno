#include <cstdint>
#include <memory>
#include <vector>

#include <pybind11/pytypes.h>

#include "uproot-custom/uproot-custom.hh"

using namespace uproot;

class JMSmartRefReader : public IReader {
private:
  const std::string m_name;
  std::shared_ptr<std::vector<int64_t>> m_entry;
  std::shared_ptr<std::vector<uint16_t>> m_pidf;

public:
  JMSmartRefReader(const std::string &name)
      : IReader(name), m_entry(std::make_shared<std::vector<int64_t>>()),
        m_pidf(std::make_shared<std::vector<uint16_t>>()) {}

  void read(BinaryBuffer &buffer) override {
    buffer.skip_TObject();
    m_pidf->push_back(buffer.read<uint16_t>());
    m_entry->push_back(buffer.read<int64_t>());
  }

  py::object data() const override {
    auto entry_array = make_array(m_entry);
    auto pidf_array = make_array(m_pidf);
    return py::make_tuple(pidf_array, entry_array);
  }
};

PYBIND11_MODULE(pyjuno_cpp, m) {
  IMPORT_UPROOT_CUSTOM_CPP;

  declare_reader<JMSmartRefReader, std::string>(m, "JMSmartRefReader");
}
