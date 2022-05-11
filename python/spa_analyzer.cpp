#include <stdexcept>

#include "analyzer.h"

const std::vector<std::string> Analyzer::OBS_FLD_NAMES = {
    "longitude", "latitude", "elevation",   "timezone",      "delta_ut1",
    "delta_t",   "pressure", "temperature", "atmos_refract",
};

void SPA_Analyzer::set_observatory(const py::kwargs &kwargs)
{
    for (auto &&fname : OBS_FLD_NAMES)
    {
        if (kwargs.contains(fname))
        {
            _observatory[fname] = kwargs.attr("get")(fname, 0.0).cast<double>();
        }

        if (_observatory.find(fname) == _observatory.end())
        {
            _observatory[fname] = 0.0;
        }
    }

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

    _observatory_set = true;
}

py::dict SPA_Analyzer::get_observatory()
{
    py::dict d(py::arg("longitude") = _observatory["longitude"],
               py::arg("latitude") = _observatory["latitude"],
               py::arg("elevation") = _observatory["elevation"],
               py::arg("timezone") = _observatory["timezone"],
               py::arg("delta_ut1") = _observatory["delta_ut1"],
               py::arg("delta_t") = _observatory["delta_t"],
               py::arg("pressure") = _observatory["pressure"],
               py::arg("temperature") = _observatory["temperature"],
               py::arg("atmos_refract") = _observatory["atmos_refract"]);

    return d;
}

py::tuple SPA_Analyzer::calc_sun_position_at(int year, int month, int day,
                                             int hour, int minute, int second)
{
    if (!_observatory_set)
        throw std::runtime_error("Observatory has not set");

    _spa.year = year;
    _spa.month = month;
    _spa.day = day;
    _spa.hour = hour;
    _spa.minute = minute;
    _spa.second = second;

    int result = spa_calculate(&_spa);

    if (result == 0)
    {
        return py::make_tuple(_spa.zenith, _spa.azimuth, _spa.jd);
    }
    else
    {
        std::string err_msg;
        switch (result)
        {
        case 1:
            err_msg = "Year Not in valid range: -2000 to 6000, " +
                      std::to_string(year);
            break;
        case 2:
            err_msg =
                "Month Not in valid range: 1 to 12, " + std::to_string(month);
            break;
        case 3:
            err_msg = "Day Not in valid range: 1 to 31, " + std::to_string(day);
            break;
        case 4:
            err_msg =
                "Hour Not in valid range: 0 to 24, " + std::to_string(hour);
            break;
        case 5:
            err_msg =
                "Minute Not in valid range: 0 to 59, " + std::to_string(minute);
            break;
        case 6:
            err_msg = "Second Not in valid range: 0 to <60, " +
                      std::to_string(second);
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
