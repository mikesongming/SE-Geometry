#include <stdexcept>

#include "spa_calculator.h"

std::vector<double> SPACalculator::calc_sun_position()
{
    if (!has_set_observatory())
        throw std::runtime_error("Observatory is unset");
    if (!has_set_local_datetime())
        throw std::runtime_error("Local datetime is unset");

    _spa.longitude = _observatory["longitude"];
    _spa.latitude = _observatory["latitude"];
    _spa.elevation = _observatory["elevation"];
    _spa.timezone = _observatory["timezone"];
    _spa.delta_ut1 = _observatory["delta_ut1"];
    _spa.delta_t = _observatory["delta_t"];
    _spa.pressure = _observatory["pressure"];
    _spa.temperature = _observatory["temperature"];
    _spa.atmos_refract = _observatory["atmos_refract"];
    _spa.function = SPA_ZA;

    _spa.year = _local_datetime[0];
    _spa.month = _local_datetime[1];
    _spa.day = _local_datetime[2];
    _spa.hour = _local_datetime[3];
    _spa.minute = _local_datetime[4];
    _spa.second = _local_datetime[5];

    int result = spa_calculate(&_spa);

    if (result == 0)
    {
        return std::vector<double>{_spa.zenith, _spa.azimuth, _spa.jd};
    }
    else
    {
        std::string err_msg;
        switch (result)
        {
        case 1:
            err_msg = "Year Not in valid range: -2000 to 6000, " +
                      std::to_string(_spa.year);
            break;
        case 2:
            err_msg = "Month Not in valid range: 1 to 12, " +
                      std::to_string(_spa.month);
            break;
        case 3:
            err_msg =
                "Day Not in valid range: 1 to 31, " + std::to_string(_spa.day);
            break;
        case 4:
            err_msg = "Hour Not in valid range: 0 to 24, " +
                      std::to_string(_spa.hour);
            break;
        case 5:
            err_msg = "Minute Not in valid range: 0 to 59, " +
                      std::to_string(_spa.minute);
            break;
        case 6:
            err_msg = "Second Not in valid range: 0 to <60, " +
                      std::to_string(_spa.second);
            break;
        case 7:
            err_msg = "Delta_t Not in valid range: -8000 to 8000 seconds, " +
                      std::to_string(_observatory["delta_t"]);
            break;
        case 8:
            err_msg = "Timezone Not in valid range: -18 to 18 hours, " +
                      std::to_string(_observatory["timezone"]);
            break;
        case 9:
            err_msg = "Longitude Not in valid range: -180 to 180 degrees, " +
                      std::to_string(_observatory["longitude"]);
            break;
        case 10:
            err_msg = "Latitude Not in valid range: -90 to 90 degrees, " +
                      std::to_string(_observatory["latitude"]);
            break;
        case 11:
            err_msg =
                "Elevation Not in valid range: -6500000 or higher meters, " +
                std::to_string(_observatory["elevation"]);
            break;
        case 12:
            err_msg = "Pressure Not in valid range: 0 to 5000 millibars, " +
                      std::to_string(_observatory["pressure"]);
            break;
        case 13:
            err_msg = "Temperature Not in valid range: -273 to 6000 degrees "
                      "Celsius, " +
                      std::to_string(_observatory["temperature"]);
            break;
        case 14:
            err_msg = "Slope Not in valid range: -360 to 360 degrees, ";
            break;
        case 15:
            err_msg = "AZM_rotation Not in valid range: -360 to 360 degrees, ";
            break;
        case 16:
            err_msg = "Atmos_Refract Not in valid range: -5 to 5 degrees, " +
                      std::to_string(_observatory["atmos_refract"]);
            break;
        case 17:
            err_msg =
                "Delta_ut1 Not in valid range: -1 to 1 second (exclusive), " +
                std::to_string(_observatory["delta_ut1"]);
            break;
        default:
            err_msg =
                "Unknown SPA validation error code " + std::to_string(result);
            break;
        }
        throw std::invalid_argument(err_msg);
    }
}
