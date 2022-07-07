set(USE_SYSTEM_TZ_DB ON CACHE INTERNAL "")
set(BUILD_SHARED_LIBS ON CACHE INTERNAL "")
set(BUILD_TZ_LIB ON CACHE INTERNAL "")

# switch off C++17 uncaught_exceptions
# add_compile_definitions(HAS_UNCAUGHT_EXCEPTIONS=FALSE)

include(FetchContent)
FetchContent_Declare(howard_hinnant_date
    GIT_REPOSITORY https://github.com/HowardHinnant/date.git
    GIT_TAG v3.0.1
)
FetchContent_MakeAvailable(howard_hinnant_date)
