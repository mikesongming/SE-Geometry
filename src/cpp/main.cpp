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

    py::class_<SPA_Calculator>(m, "SPA_Calculator")
        .def(py::init<>())
        .def("get_observatory", &SPA_Calculator::get_observatory)
        .def("set_observatory", &SPA_Calculator::set_observatory)
        .def("has_set_observatory", &SPA_Calculator::has_set_observatory)
        .def("calc_sun_position_at", &SPA_Calculator::calc_sun_position_at);
}
