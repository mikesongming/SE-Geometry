#if !defined(SPA_INTERFACE_H)
#define SPA_INTERFACE_H

#include <string>
#include <chrono>

#include <pybind11/pybind11.h>

namespace py = pybind11;
using system_time = std::chrono::system_clock::time_point;

struct SunPositionAnalysis
{
    // Observer local time
    int year;     
    int month;    
    int day;      
    int hour;     
    int minute;   
    double second;
    double timezone;

    // Observer local position
    double longitude;
    double latitude;
    double elevation;

    // Observer local climate
    double pressure;
    double temperature;
    double atmos_refract;   

    // time difference
    double delta_ut1;
    double delta_t;

    //---------------------Final Topocentric OUTPUT VALUES------------------------
    double jd;
    double zenith;
    double azimuth;

    double suntransit;
    double sunrise;   
    double sunset;    

    static SunPositionAnalysis parse(const py::kwargs &kwargs);
    // SunPositionAnalysis(const system_time &dt, const py::kwargs &kwargs);
    void print_input();
    void print_output();
    int do_calculation(bool with_sun_rts = false);

private:
    bool _with_sun_rts;

    SunPositionAnalysis(
        int year, int month, int day , int hour, int minute,
        double second, double timezone, double longitude, double latitude, double elevation,
        double delta_t, double pressure,double temperature,double atmos_refract
    ): year(year), month(month), day(day), hour(hour), minute(minute), second(second),
    timezone(timezone), longitude(longitude), latitude(latitude), elevation(elevation),
    delta_ut1(0), delta_t(delta_t), pressure(pressure), temperature(temperature),
    atmos_refract(atmos_refract), jd(0.0), zenith(0.0), azimuth(0.0),
    sunrise(0.0), suntransit(0.0), sunset(0.0), _with_sun_rts(false) {};
};

#endif // SPA_INTERFACE_H