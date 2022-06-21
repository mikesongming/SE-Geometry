#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "analyzer.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_fseg, m)
{
    m.doc() = R"pbdoc(
    Solar-Earth analysis algorithms
    -----------------------------
    )pbdoc";

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif

    py::class_<SPA_Analyzer>(m, "SPA_Analyzer")
        .def(py::init<>())
        .def("get_observatory", &SPA_Analyzer::get_observatory)
        .def("set_observatory", &SPA_Analyzer::set_observatory)
        .def("has_set_observatory", &SPA_Analyzer::has_set_observatory)
        .def("calc_sun_position_at", &SPA_Analyzer::calc_sun_position_at);
}
