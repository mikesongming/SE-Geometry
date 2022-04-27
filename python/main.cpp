#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "spa_interface.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_sun_earth_geometry, m) {
    m.doc() = R"pbdoc(
    Solar-Earth analysis algorithms
    -----------------------------
    )pbdoc";

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif

    py::class_<SunPositionAnalysis>(m, "SunPositionAnalysis")
        .def(py::init(&SunPositionAnalysis::parse))
        .def(py::init(
            [](const std::string &dt_str, const py::kwargs &kwargs)
            {
                auto spa = SunPositionAnalysis::parse(kwargs);

                py::object datetime = py::module_::import("datetime").attr("datetime");
                py::object fmt = py::str("%Y-%m-%d %H:%M:%S");
                py::object dt = datetime.attr("strptime")(dt_str, fmt);
                spa.year = dt.attr("year").cast<int>();
                spa.month = dt.attr("month").cast<int>();
                spa.day = dt.attr("day").cast<int>();
                spa.hour = dt.attr("hour").cast<int>();
                spa.minute = dt.attr("minute").cast<int>();
                spa.second = dt.attr("second").cast<double>();

                return spa;}))
        .def_readwrite("year", &SunPositionAnalysis::year)
        .def_readwrite("month", &SunPositionAnalysis::month)
        .def_readwrite("day", &SunPositionAnalysis::day)
        .def_readwrite("hour", &SunPositionAnalysis::hour)
        .def_readwrite("minute", &SunPositionAnalysis::minute)
        .def_readwrite("second", &SunPositionAnalysis::second)
        .def_readwrite("timezone", &SunPositionAnalysis::timezone)
        .def_readwrite("longitude", &SunPositionAnalysis::longitude)
        .def_readwrite("latitude", &SunPositionAnalysis::latitude)
        .def_readwrite("elevation", &SunPositionAnalysis::elevation)
        .def_readwrite("pressure", &SunPositionAnalysis::pressure)
        .def_readwrite("temperature", &SunPositionAnalysis::temperature)
        .def_readwrite("atmos_refract", &SunPositionAnalysis::atmos_refract)
        .def_readwrite("delta_t", &SunPositionAnalysis::delta_t)
        .def_readonly("jd", &SunPositionAnalysis::jd)
        .def_readonly("zenith", &SunPositionAnalysis::zenith)
        .def_readonly("azimuth", &SunPositionAnalysis::azimuth)
        .def_readonly("sunrise", &SunPositionAnalysis::sunrise)
        .def_readonly("suntransit", &SunPositionAnalysis::suntransit)
        .def_readonly("sunset", &SunPositionAnalysis::sunset)
        .def("print_input", &SunPositionAnalysis::print_input)
        .def("print_output", &SunPositionAnalysis::print_output)
        .def("__call__", &SunPositionAnalysis::do_calculation,
             py::arg("with_sun_rts") = false);
}