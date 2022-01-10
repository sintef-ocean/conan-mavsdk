from conans import ConanFile, CMake, tools
from conans.model.version import Version


class MAVSDKConan(ConanFile):
    name = "mavsdk"
    version = "0.39.0"
    license = "MIT"
    author = "SINTEF Ocean"
    homepage = "https://mavsdk.mavlink.io/main/en/"
    url = "https://github.com/mavlink/MAVSDK.git"
    description = "C++ library to interface with MAVLink systems"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"
    requires = [
        "jsoncpp/1.9.5",
        "tinyxml2/9.0.0",
        "libcurl/7.80.0"
        ]
    
    options = {
        "shared": [True, False]
        }
    default_options = {
        "shared": False
        }

    source_folder = "mavsdk-{}".format(version)

    scm = {
        "type": "git",
        "subfolder": source_folder,
        "url": "https://github.com/mavlink/MAVSDK.git",
        "revision": "v{}".format(version),
        "submodule": "recursive"
        }

    def requirements(self):
        if self.settings.os != "iOS":
            self.requires("zlib/1.2.11")

    def configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["SUPERBUILD"] = "OFF"
        cmake.definitions["BUILD_MAVSDK_SERVER"] = "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = \
            "ON" if self.options.shared else "OFF"
       
        cmake.configure()
        return cmake

    def source(self):
        tools.replace_in_file("{}/src/CMakeLists.txt".format(self.source_folder),
                              "project(mavsdk)",
                              '''project(mavsdk)
# BEGIN CONAN PATCH
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
link_libraries(${CONAN_LIBS})
# END CONAN PATCH''')

        tools.replace_in_file("{}/src/core/connection.h".format(self.source_folder),
                              "#include <unordered_set>",
                              '''#include <unordered_set>
// BEGIN CONAN PATCH
#include <atomic>
// END CONAN PATCH''')

        tools.replace_in_file("{}/src/cmake/unit_tests.cmake".format(self.source_folder),
                            "JsonCpp::jsoncpp",
                            '''# BEGIN CONAN PATCH
jsoncpp::jsoncpp
# END CONAN PATCH''')

        tools.replace_in_file("{}/src/plugins/mission_raw/CMakeLists.txt".format(self.source_folder),
                            "JsonCpp::jsoncpp",
                            '''# BEGIN CONAN PATCH
jsoncpp::jsoncpp
# END CONAN PATCH''')

        tools.replace_in_file("{}/src/plugins/mission/CMakeLists.txt".format(self.source_folder),
                            "JsonCpp::jsoncpp",
                            '''# BEGIN CONAN PATCH
jsoncpp::jsoncpp
# END CONAN PATCH''')

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.name = 'MAVSDK'
        libs = [
                "mavsdk",
                "mavsdk_action",
                "mavsdk_action_server",
                "mavsdk_calibration", 
                "mavsdk_camera",
                "mavsdk_failure",
                "mavsdk_follow_me",
                "mavsdk_ftp",
                "mavsdk_geofence",
                "mavsdk_gimbal",
                "mavsdk_info",
                "mavsdk_log_files",
                "mavsdk_manual_control",
                "mavsdk_mission",
                "mavsdk_mission_raw_server", 
                "mavsdk_mocap",
                "mavsdk_offboard",
                "mavsdk_param",
                "mavsdk_server_utility",
                "mavsdk_shell",
                "mavsdk_telemetry",
                "mavsdk_telemetry_server",
                "mavsdk_tracking_server",
                "mavsdk_transponder",
                "mavsdk_tune"
            ]

        if self.settings.compiler == "Visual Studio" \
           and self.settings.build_type == "Debug":
            self.cpp_info.libs = [lib + "d" for lib in libs]
        else:
            self.cpp_info.libs = libs

        self.cpp_info.includedirs.extend([
            "include/mavsdk",
            "include/mavsdk/plugins/action",
            "include/mavsdk/plugins/action_server",
            "include/mavsdk/plugins/calibration",
            "include/mavsdk/plugins/camera",
            "include/mavsdk/plugins/failure",
            "include/mavsdk/plugins/follow_me",
            "include/mavsdk/plugins/ftp",
            "include/mavsdk/plugins/geofence",
            "include/mavsdk/plugins/gimbal",
            "include/mavsdk/plugins/info",
            "include/mavsdk/plugins/log_files",
            "include/mavsdk/plugins/manual_control",
            "include/mavsdk/plugins/mavlink_passthrough",
            "include/mavsdk/plugins/mission",
            "include/mavsdk/plugins/mission_raw",
            "include/mavsdk/plugins/mission_raw_server",
            "include/mavsdk/plugins/mocap",
            "include/mavsdk/plugins/offboard",
            "include/mavsdk/plugins/param",
            "include/mavsdk/plugins/server_utility",
            "include/mavsdk/plugins/shell",
            "include/mavsdk/plugins/telemetry",
            "include/mavsdk/plugins/tracking_server",
            "include/mavsdk/plugins/transponder",
            "include/mavsdk/plugins/tune",
        ])