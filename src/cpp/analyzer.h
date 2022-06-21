#pragma once

#include <pybind11/pybind11.h>

#include <map>
#include <string>
#include <vector>

#include "SPA/spa.h"

namespace py = pybind11;

class Analyzer
{
  public:
    virtual py::dict get_observatory() = 0;
    virtual void set_observatory(const py::kwargs &kwargs) = 0;
    virtual py::tuple calc_sun_position_at(int year, int month, int day,
                                           int hour, int minute,
                                           int second) = 0;
    bool has_set_observatory()
    {
        return _observatory_set;
    };
    static const std::vector<std::string> OBS_FLD_NAMES;

  protected:
    bool _observatory_set = false;
};

class SPA_Analyzer : public Analyzer
{
  public:
    py::dict get_observatory();
    void set_observatory(const py::kwargs &kwargs);
    py::tuple calc_sun_position_at(int year, int month, int day, int hour,
                                   int minute, int second);

  private:
    std::map<std::string, double> _observatory;
    spa_data _spa;
};
