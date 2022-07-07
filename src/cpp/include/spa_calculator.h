#pragma once

#include "algorithm.h"
#include "SPA/spa.h"

namespace py = pybind11;

class SPACalculator : public Algorithm
{
  public:
    std::string name() override { return "SPA"; };
    std::vector<double> calc_sun_position() override;

  private:
    spa_data _spa;
};

class PySPACaculator : public SPACalculator
{
  public:
    using SPACalculator::SPACalculator;

    std::string name() override
    {
        PYBIND11_OVERRIDE(std::string, SPACalculator, name, );
    }

    std::vector<double> calc_sun_position() override
    {
        PYBIND11_OVERRIDE(std::vector<double>, SPACalculator, calc_sun_position, );
    }
};
