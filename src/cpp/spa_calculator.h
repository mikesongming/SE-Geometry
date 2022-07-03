#pragma once

#include "algorithm.h"
#include "SPA/spa.h"

namespace py = pybind11;

class SPACalculator : public Algorithm
{
  public:
    std::vector<double> calc_sun_position() override;

  private:
    spa_data _spa;
};

class PySPACaculator : public SPACalculator
{
  public:
    using SPACalculator::SPACalculator;

    std::vector<double> calc_sun_position() override
    {
        PYBIND11_OVERLOAD(std::vector<double>, SPACalculator,
                          calc_sun_position, );
    }
};
