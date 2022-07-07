#include "algorithm.h"

#include "date/tz.h"
#include <sstream>

const std::vector<std::string> Algorithm::OBS_FIELDS = {
    "longitude", "latitude", "elevation",   "timezone",      "delta_ut1",
    "delta_t",   "pressure", "temperature", "atmos_refract",
};

void Algorithm::set_observatory(const py::kwargs &kwargs)
{
    bool found = false;

    for (auto &&key : Algorithm::OBS_FIELDS)
    {
        if (kwargs.contains(key))
        {
            _observatory[key] = kwargs.attr("get")(key, 0.0).cast<double>();
            found = true;
        }
    }

    if (found)
    {
        _observatory_set = true;
    }
}

void Algorithm::set_observatory(const std::map<std::string, double> &obs_m)
{
    bool found = false;

    for (auto &&key : Algorithm::OBS_FIELDS)
    {
        auto item = obs_m.find(key);
        if (item != obs_m.end())
        {
            _observatory[key] = item->second;
            found = true;
        }
    }

    if (found)
    {
        _observatory_set = true;
    }
}

void Algorithm::set_local_datetime(const std::array<unsigned, 6> &dt_arr)
{
    _local_datetime = dt_arr;

    _local_datetime_set = true;
}
void Algorithm::set_local_datetime(const std::string &dt_str)
{
    std::istringstream in{dt_str};
    std::chrono::system_clock::time_point tp;
    in >> date::parse("%Y-%m-%d %H:%M:%S", tp);

    if (in.fail())
    {
        std::string err_msg = "Mismatched datetime string: '" + dt_str + "'";
        throw std::invalid_argument(err_msg);
    }

    auto dp = date::floor<date::days>(tp);
    auto ymd = date::year_month_day{dp};
    auto time = date::make_time(
        std::chrono::duration_cast<std::chrono::milliseconds>(tp - dp));

    unsigned year = static_cast<unsigned>(static_cast<int>(ymd.year()));
    unsigned month = static_cast<unsigned>(ymd.month());
    unsigned day = static_cast<unsigned>(ymd.day());
    unsigned hour = static_cast<unsigned>(time.hours().count());
    unsigned minute = static_cast<unsigned>(time.minutes().count());
    unsigned second = static_cast<unsigned>(time.seconds().count());

    _local_datetime = {year, month, day, hour, minute, second};
    _local_datetime_set = true;
}
void Algorithm::set_local_datetime(
    const std::chrono::system_clock::time_point &dt_tp)
{
    /*
     * pybind11 conversion of python datetime.datetime will ignore tzinfo,
     * thus to use date/tz.h to recover time zone offset
     */
    auto z_tp = date::make_zoned(date::current_zone(), dt_tp);
    auto lt = z_tp.get_local_time();

    auto dp = date::floor<date::days>(lt);
    auto ymd = date::year_month_day{dp};
    auto time = date::make_time(
        std::chrono::duration_cast<std::chrono::milliseconds>(lt - dp));

    unsigned year = static_cast<unsigned>(static_cast<int>(ymd.year()));
    unsigned month = static_cast<unsigned>(ymd.month());
    unsigned day = static_cast<unsigned>(ymd.day());
    unsigned hour = static_cast<unsigned>(time.hours().count());
    unsigned minute = static_cast<unsigned>(time.minutes().count());
    unsigned second = static_cast<unsigned>(time.seconds().count());

    _local_datetime = {year, month, day, hour, minute, second};
    _local_datetime_set = true;
}
