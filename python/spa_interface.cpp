#include <cstdio>
#include <pybind11/pybind11.h>

#include "spa_interface.h"
#include "SPA/spa.h"

namespace py = pybind11;

SunPositionAnalysis SunPositionAnalysis::parse(const py::kwargs &kwargs)
{
    auto year = kwargs.attr("get")("year", 0).cast<int>();
    auto month = kwargs.attr("get")("month", 0).cast<int>();
    auto day = kwargs.attr("get")("day", 0).cast<int>();
    auto hour = kwargs.attr("get")("hour", 0).cast<int>();
    auto minute = kwargs.attr("get")("minute", 0).cast<int>();

    auto second = kwargs.attr("get")("second", 0.0).cast<double>();
    auto timezone = kwargs.attr("get")("timezone", 0.0).cast<double>();
    auto longitude = kwargs.attr("get")("longitude", 0.0).cast<double>();
    auto latitude = kwargs.attr("get")("latitude", 0.0).cast<double>();
    auto elevation = kwargs.attr("get")("elevation", 0.0).cast<double>();
    auto pressure = kwargs.attr("get")("pressure", 0.0).cast<double>();
    auto temperature = kwargs.attr("get")("temperature", 0.0).cast<double>();
    auto atmos_refract = kwargs.attr("get")("atmos_refract", 0.5667).cast<double>();
    auto delta_t = kwargs.attr("get")("delta_t", 0.0).cast<double>();
    auto delta_ut1 = kwargs.attr("get")("delta_ut1", 0.0).cast<double>();

    return SunPositionAnalysis(year, month, day, hour, minute, second, timezone,
                               longitude, latitude, elevation, delta_t,
                               pressure, temperature, atmos_refract);
}

void SunPositionAnalysis::print_input() {
    printf("Year:           %d\n", year);     
    printf("Month:          %d\n", month);    
    printf("Day:            %d\n", day);      
    printf("Hour:           %d\n", hour);     
    printf("Minute:         %d\n", minute);   
    printf("Second:         %.6f\n", second);
    printf("Timezone:       %.6f\n", timezone);
    printf("Longitude:      %.6f\n", longitude);
    printf("Latitude:       %.6f\n", latitude);
    printf("Elevation:      %.6f\n", elevation);
    printf("Pressure:       %.6f\n", pressure);
    printf("Temperature:    %.6f\n", temperature);
    printf("Atmos_Refract:  %.6f\n", atmos_refract);   
    printf("Delta T:        %.6f\n", delta_t);
}

void SunPositionAnalysis::print_output() {
    float min, sec;

    printf("Julian Day:    %.6f\n", jd);
    printf("Zenith:        %.6f degrees\n", zenith);
    printf("Azimuth:       %.6f degrees\n", azimuth);

    if (this->_with_sun_rts)
    {
        min = 60.0*(sunrise - (int)(sunrise));
        sec = 60.0*(min - (int)min);
        printf("Sunrise:       %02d:%02d:%02d Local Time\n", (int)(sunrise), (int)min, (int)sec);
        
        min = 60.0*(suntransit - (int)(suntransit));
        sec = 60.0*(min - (int)min);
        printf("Suntransit:    %02d:%02d:%02d Local Time\n", (int)(suntransit), (int)min, (int)sec);
        
        min = 60.0*(sunset - (int)(sunset));
        sec = 60.0*(min - (int)min);
        printf("Sunset:        %02d:%02d:%02d Local Time\n", (int)(sunset), (int)min, (int)sec);
    }
}

int SunPositionAnalysis::do_calculation(bool with_sun_rts) {
    this->_with_sun_rts = with_sun_rts;
    spa_data spa;
    int result;

    spa.year          = this->year;
    spa.month         = this->month;
    spa.day           = this->day;
    spa.hour          = this->hour;
    spa.minute        = this->minute;
    spa.second        = this->second;
    spa.timezone      = this->timezone;
    spa.delta_ut1     = this->delta_ut1;
    spa.delta_t       = this->delta_t;
    spa.longitude     = this->longitude;
    spa.latitude      = this->latitude;
    spa.elevation     = this->elevation;
    spa.pressure      = this->pressure;
    spa.temperature   = this->temperature;
    spa.atmos_refract = this->atmos_refract;
    spa.function      = this->_with_sun_rts ? SPA_ZA_RTS : SPA_ZA;
    
    result = spa_calculate(&spa);

    if (result == 0)
    {
        this->jd = spa.jd;
        this->zenith = spa.zenith;
        this->azimuth = spa.azimuth;
        this->suntransit = spa.suntransit;
        this->sunrise = spa.sunrise;
        this->sunset = spa.sunset;
    } else {
        printf("SPA Error Code: %d\n", result);
        
        std::string err_msg; 
        switch (result)
        {
        case 1:
            err_msg = "Year Not in valid range: -2000 to 6000";
            break;
        case 2:
            err_msg = "Month Not in valid range: 1 to 12";
            break;
        case 3:
            err_msg = "Day Not in valid range: 1 to 31";
            break;
        case 4:
            err_msg = "Hour Not in valid range: 0 to 24";
            break;
        case 5:
            err_msg = "Minute Not in valid range: 0 to 59";
            break;
        case 6:
            err_msg = "Second Not in valid range: 0 to <60";
            break;
        case 7:
            err_msg = "Delta_t Not in valid range: -8000 to 8000 seconds";
            break;
        case 8:
            err_msg = "Timezone Not in valid range: -18 to 18 hours";
            break;
        case 9:
            err_msg = "Longitude Not in valid range: -180 to 180 degrees";
            break;
        case 10:
            err_msg = "Latitude Not in valid range: -90 to 90 degrees";
            break;
        case 11:
            err_msg = "Elevation Not in valid range: -6500000 or higher meters";
            break;
        case 12:
            err_msg = "Pressure Not in valid range: 0 to 5000 millibars";
            break;
        case 13:
            err_msg = "Temperature Not in valid range: -273 to 6000 degrees Celsius";
            break;
        case 14:
            err_msg = "Slope Not in valid range: -360 to 360 degrees";
            break;
        case 15:
            err_msg = "AZM_rotation Not in valid range: -360 to 360 degrees";
            break;
        case 16:
            err_msg = "Atmos_Refract Not in valid range: -5 to 5 degrees";
            break;
        case 17:
            err_msg = "Delta_ut1 Not in valid range: -1 to 1 second (exclusive)";
            break;
        default:
            err_msg = "Unknown SPA validation error code " + std::to_string(result);
            break;
        }
        throw std::invalid_argument(err_msg);
    }
    
    return result;
}