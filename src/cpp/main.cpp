#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // necessary for vector conversion
#include <pybind11/chrono.h> // necessary for datetime conversion

#include "algorithm.h"
#include "spa_calculator.h"

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

    py::class_<Algorithm, PyAlgorithm>(m, "Algorithm")
        .def(py::init<>())
        .def_readonly_static("OBS_FIELDS", &Algorithm::OBS_FIELDS)
        .def("has_set_observatory", &Algorithm::has_set_observatory)
        .def("get_observatory", &Algorithm::get_observatory)
        .def("set_observatory",
             py::overload_cast<const py::kwargs &>(&Algorithm::set_observatory),
             "set observatory by kwargs")
        .def("set_observatory",
             py::overload_cast<const std::map<std::string, double> &>(
                 &Algorithm::set_observatory),
             "set observatory by dict")
        .def("has_set_local_datetime", &Algorithm::has_set_local_datetime)
        .def("get_local_datetime", &Algorithm::get_local_datetime)
        .def("set_local_datetime",
             py::overload_cast<const std::array<unsigned, 6> &>(
                 &Algorithm::set_local_datetime),
             "set observatory by array")
        .def("set_local_datetime",
             py::overload_cast<const std::string &>(
                 &Algorithm::set_local_datetime),
             "set observatory by formatted string")
        .def("set_local_datetime",
             py::overload_cast<const std::chrono::system_clock::time_point &>(
                 &Algorithm::set_local_datetime),
             "set observatory by datetime")
        .def_property_readonly("name", &Algorithm::name)
        .def("calc_sun_position", &Algorithm::calc_sun_position);

    py::class_<SPACalculator, Algorithm, PySPACaculator>(m, "SPACalculator")
        .def(py::init<>())
        .def_property_readonly("name", &SPACalculator::name)
        .def("calc_sun_position", &SPACalculator::calc_sun_position);
}
