#include <cstdint>
#include <memory>
#include <vector>

#include <pybind11/pytypes.h>

#include "uproot-custom/uproot-custom.hh"

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

    void read( BinaryBuffer& buffer ) override {
        buffer.skip_TObject();
        m_pidf->push_back( buffer.read<uint16_t>() );
        m_entry->push_back( buffer.read<int64_t>() );
    }

    py::object data() const override {
        auto entry_array = make_array( m_entry );
        auto pidf_array  = make_array( m_pidf );
        return py::make_tuple( pidf_array, entry_array );
    }
};

class AnyJMClassReader : public IReader {
  private:
    vector<SharedReader> m_element_readers;

  public:
    AnyJMClassReader( string name, vector<SharedReader> element_readers )
        : IReader( name ), m_element_readers( element_readers ) {}

    void read( BinaryBuffer& buffer ) override {
        buffer.read_obj_header();
        auto fNBytes   = buffer.read_fNBytes();
        auto start_pos = buffer.get_cursor();
        auto end_pos   = buffer.get_cursor() + fNBytes;

        auto fVersion = buffer.read_fVersion();

        for ( auto& reader : m_element_readers )
        {
            debug_printf( "AnyJMClassReader %s: reading %s\n", m_name.c_str(),
                          reader->name().c_str() );
            debug_printf( buffer );
            reader->read( buffer );
        }

        if ( buffer.get_cursor() != end_pos )
        {
            stringstream msg;
            msg << "AnyJMClassReader: Invalid read length for " << name() << "! Expect "
                << end_pos - start_pos << ", got " << buffer.get_cursor() - start_pos;
            throw std::runtime_error( msg.str() );
        }
    }

    py::object data() const override {
        py::list res;
        for ( auto& reader : m_element_readers ) { res.append( reader->data() ); }
        return res;
    }
};

class AnyCLHEPClassReader : public IReader {
  private:
    vector<SharedReader> m_element_readers; ///< The element readers for the Any class.

  public:
    AnyCLHEPClassReader( string name, vector<SharedReader> element_readers )
        : IReader( name ), m_element_readers( element_readers ) {}

    void read( BinaryBuffer& buffer ) override {
        auto fNBytes   = buffer.read_fNBytes();
        auto start_pos = buffer.get_cursor();
        auto end_pos   = buffer.get_cursor() + fNBytes;

        auto fVersion = buffer.read_fVersion();
        buffer.skip( 4 ); // unknown

        for ( auto& reader : m_element_readers )
        {
            debug_printf( "AnyCLHEPClassReader %s: reading %s\n", m_name.c_str(),
                          reader->name().c_str() );
            debug_printf( buffer );
            reader->read( buffer );
        }
    }

    uint32_t read_many_memberwise( BinaryBuffer& buffer, const int64_t count ) override {
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
            debug_printf( buffer );
            reader->read_many( buffer, count );
        }

        return count;
    }

    py::object data() const override {
        py::list res;
        for ( auto& reader : m_element_readers ) { res.append( reader->data() ); }
        return res;
    }
};

PYBIND11_MODULE( pyjuno_cpp, m ) {
    IMPORT_UPROOT_CUSTOM_CPP;

    declare_reader<JMSmartRefReader, string>( m, "JMSmartRefReader" );
    declare_reader<AnyJMClassReader, string, vector<SharedReader>>( m, "AnyJMClassReader" );
    declare_reader<AnyCLHEPClassReader, string, vector<SharedReader>>( m,
                                                                       "AnyCLHEPClassReader" );
}
