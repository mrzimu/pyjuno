#include <cstdint>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <pybind11/pytypes.h>
#include <uproot-custom/uproot-custom.hh>

using namespace uproot;
using namespace std;

class JMSmartRefReader : public IReader {
  private:
    const string m_name;
    shared_ptr<vector<int64_t>> m_entry;
    shared_ptr<vector<uint16_t>> m_pidf;

  public:
    JMSmartRefReader( const string& name )
        : IReader( name )
        , m_entry( make_shared<vector<int64_t>>() )
        , m_pidf( make_shared<vector<uint16_t>>() ) {}

    void read( BinaryStream& stream ) override {
        stream.skip_TObject();
        m_pidf->push_back( stream.read<uint16_t>() );
        m_entry->push_back( stream.read<int64_t>() );
    }

    py::object data() const override {
        auto entry_array = make_array( m_entry );
        auto pidf_array  = make_array( m_pidf );
        return py::make_tuple( pidf_array, entry_array );
    }
};

class AnyCLHEPClassReader : public IReader {
  private:
    vector<SharedReader> m_element_readers; ///< The element readers for the Any class.

  public:
    AnyCLHEPClassReader( string name, vector<SharedReader> element_readers )
        : IReader( name ), m_element_readers( element_readers ) {}

    void read( BinaryStream& stream ) override {
        auto fNBytes   = stream.read_fNBytes();
        auto start_pos = stream.get_cursor();
        auto end_pos   = stream.get_cursor() + fNBytes;

        auto fVersion = stream.read_fVersion();
        stream.skip( 4 ); // unknown

        for ( auto& reader : m_element_readers )
        {
            debug_printf( "AnyCLHEPClassReader %s: reading %s\n", m_name.c_str(),
                          reader->name().c_str() );
            debug_printf( stream );
            reader->read( stream );
        }

        if ( stream.get_cursor() != end_pos )
        {
            stringstream msg;
            msg << "AnyCLHEPClassReader: Invalid read length for " << name() << "! Expect "
                << end_pos - start_pos << ", got " << stream.get_cursor() - start_pos;
            throw std::runtime_error( msg.str() );
        }
    }

    uint32_t read_many_memberwise( BinaryStream& stream, const int64_t count ) override {
        if ( count < 0 )
        {
            stringstream msg;
            msg << name() << "::read_many_memberwise with negative count: " << count;
            throw std::runtime_error( msg.str() );
        }

        for ( auto& reader : m_element_readers )
        {
            debug_printf( "AnyCLHEPClassReader %s: reading memberwise %s\n", m_name.c_str(),
                          reader->name().c_str() );
            debug_printf( stream );
            reader->read_many( stream, count );
        }

        return count;
    }

    py::object data() const override {
        py::list res;
        for ( auto& reader : m_element_readers ) { res.append( reader->data() ); }
        return res;
    }
};

/// Convert an entry buffer to a count array. The entry buffer in Python is like:
/// ```python
/// {'node0-offsets': array([ 0,  9, 18, 27, 36, 45, 54, 63, 72, 81, 90]),
/// 'node1-index': array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
///        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
///        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
///        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
///        68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
///        85, 86, 87, 88, 89]),
/// 'node2-data': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
///        2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
///        4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7,
///        7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9,
///        9, 9])}
/// ```
py::array_t<int64_t> entry_buffer_to_count( py::dict entry_buffer, int64_t n_cols ) {
    auto offsets = entry_buffer["node0-offsets"].cast<py::array_t<int64_t>>();
    auto index   = entry_buffer["node1-index"].cast<py::array_t<int64_t>>();
    auto data    = entry_buffer["node2-data"].cast<py::array_t<int64_t>>();

    auto offsets_ptr = offsets.data();
    auto index_ptr   = index.data();
    auto data_ptr    = data.data();

    auto len = offsets.size() - 1;
    py::array_t<int64_t> res( len * n_cols );
    res =
        res.reshape( { static_cast<py::ssize_t>( len ), static_cast<py::ssize_t>( n_cols ) } );

    auto res_ptr = res.mutable_data();
    memset( res_ptr, 0, sizeof( int64_t ) * len * n_cols );

    for ( int64_t i = 0; i < len; i++ )
    {
        auto start = offsets_ptr[i];
        auto end   = offsets_ptr[i + 1];
        for ( int64_t j = 0; j < end - start; j++ )
        {
            auto cur_idx            = index_ptr[start + j];
            res_ptr[i * n_cols + j] = data_ptr[cur_idx] == -1 ? 0 : 1;
        }
    }

    return res;
}

PYBIND11_MODULE( pyjuno_cpp, m ) {
    IMPORT_UPROOT_CUSTOM_CPP;

    declare_reader<JMSmartRefReader, string>( m, "JMSmartRefReader" );
    declare_reader<AnyCLHEPClassReader, string, vector<SharedReader>>( m,
                                                                       "AnyCLHEPClassReader" );

    m.def( "entry_buffer_to_count", &entry_buffer_to_count,
           "Convert an entry buffer to a count array" );
}
