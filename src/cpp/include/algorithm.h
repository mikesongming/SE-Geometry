#pragma once

#include <pybind11/pybind11.h>

#include <map>
#include <string>
#include <vector>
#include <array>
#include <chrono>

namespace py = pybind11;

class Algorithm
{
  public:
    virtual ~Algorithm() = default;

    static const std::vector<std::string> OBS_FIELDS;

    std::map<std::string, double> get_observatory()
    {
        return _observatory;
    };
    void set_observatory(const py::kwargs &kwargs);
    void set_observatory(const std::map<std::string, double> &obs_m);
    bool has_set_observatory()
    {
        return _observatory_set;
    };

    std::array<unsigned, 6> get_local_datetime()
    {
        return _local_datetime;
    };
    void set_local_datetime(const std::array<unsigned, 6> &dt_arr);
    void set_local_datetime(const std::string &dt_str);
    void set_local_datetime(const std::chrono::system_clock::time_point &dt_tp);
    bool has_set_local_datetime()
    {
        return _local_datetime_set;
    };

    virtual std::string name() = 0;
    virtual std::vector<double> calc_sun_position() = 0;

  protected:
    bool _observatory_set = false;
    bool _local_datetime_set = false;
    std::map<std::string, double> _observatory;
    std::array<unsigned, 6> _local_datetime;
};

/*
 * Trampoline class demanded by pybind11
 */
class PyAlgorithm : public Algorithm
{
  public:
    using Algorithm::Algorithm;

    std::string name() override
    {
        PYBIND11_OVERRIDE_PURE(std::string, Algorithm, name, );
    }

    std::vector<double> calc_sun_position() override
    {
        PYBIND11_OVERRIDE_PURE(std::vector<double>, Algorithm, calc_sun_position, );
    }
};
