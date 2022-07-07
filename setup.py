import os
import platform
import re
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
from pathlib import Path

import wget
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


def download_and_extract_tzdata2022a(tempdir: Path):
    iana_url = "https://data.iana.org/time-zones/releases/tzdata2022a.tar.gz"
    local_iana_file = tempdir.joinpath(Path(iana_url).name)

    wget.download(iana_url, str(local_iana_file))
    local_tzdata_dir = tempdir.joinpath(Path(Path(local_iana_file.name).stem).stem)

    with tarfile.open(local_iana_file, "r:gz") as tar:
        tar.extractall(local_tzdata_dir)

    return local_tzdata_dir


def download_windows_mapping_file(tempdir: Path):
    url = "/".join(
        [
            "https://raw.githubusercontent.com/unicode-org/cldr",
            "main/common/supplemental/windowsZones.xml",
        ]
    )
    local_file = tempdir.joinpath(Path(url).name)

    wget.download(url, str(local_file))
    return local_file


def pack_hhdate_tzdata(tzdata_dir: Path, tzdata2022a_dir: Path, mapping_file: Path):
    if not tzdata_dir.exists():
        tzdata2022a_dir.rename(tzdata_dir)
        mapping_file.rename(tzdata_dir.joinpath(mapping_file.name))
        return tzdata_dir
    else:
        return None


def print_tzdata(tzdata_dir: Path):
    for child in tzdata_dir.iterdir():
        print(child)
        if child.is_dir():
            for _c in child.iterdir():
                print(_c)


def download_tzdata():
    tzdata_dir = Path().home().joinpath("Downloads", "tzdata")
    if tzdata_dir.exists():
        print(f"{tzdata_dir} already exists, skip download.")
    else:
        print("Downloading tzdata for Windows")
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tempDir:
            tempDir = Path(tempDir)
            tzdata2022a_dir = download_and_extract_tzdata2022a(tempDir)
            mapping_file = download_windows_mapping_file(tempDir)
            pack_hhdate_tzdata(tzdata_dir, tzdata2022a_dir, mapping_file)
            if tzdata_dir:
                print_tzdata(tzdata_dir)


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection & inclusion of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # SDIST_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
        ]
        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        # In this example, we pass in the version to C++. You might not need to.
        cmake_args += [f"-DSDIST_VERSION_INFO={self.distribution.get_version()}"]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator or cmake_generator == "Ninja":
                try:
                    import ninja  # noqa: F401

                    ninja_executable_path = os.path.join(ninja.BIN_DIR, "ninja")
                    cmake_args += [
                        "-GNinja",
                        f"-DCMAKE_MAKE_PROGRAM:FILEPATH={ninja_executable_path}",
                    ]
                except ImportError:
                    pass

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                    # DLL are treated as RUNTIME in cmake
                    f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                    # .exp and .lib files to be packaged into wheel too
                    f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
                ]
                build_args += ["--config", cfg]

            assert cfg == "Release", "MSVC only support Release build-type"
            sysconfig.get_config_vars()["Py_DEBUG"] = False

        if platform.platform().startswith("macOS"):
            macosx_version_min = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")
            if macosx_version_min:
                # Anaconda currently set macosx_version_min='10.9'
                # which is not compatible with C++17 on MacOSX
                macosx_version_min = "10.12"
                cmake_args += [
                    "-DCMAKE_OSX_DEPLOYMENT_TARGET={}".format(macosx_version_min)
                ]

            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]
        elif platform.platform().startswith("Windows"):
            try:
                download_tzdata()
            except Exception as e:
                print("Failed to download tzdata for Windows", file=sys.stderr)
                print(type(e), "::", e, file=sys.stderr)
                exit(1)

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += [f"-j{self.parallel}"]

        build_temp = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=build_temp)


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    packages=find_packages(where="src/python"),
    package_dir={"fseg": "src/python/fseg"},
    ext_package="fseg.impl",
    ext_modules=[CMakeExtension("_fseg")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    python_requires=">=3.10",
    platforms=[
        "cp310-macosx-10_12-x86_64",
        "cp310-manylinux2014_x86_64",
        "cp310-win_amd64",
    ],
)
