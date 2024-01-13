from typing import List

from vs_macro_to_cmake_macro import converter, get_vs_configuration_type_to_cmake_type
from source_parsers import SourceParser, IncludeParser


class Configuration:
    def __init__(self, name: str, platform: str):
        self.name = name
        self.platform = platform
        self._configuration = ""
        self._out_dir = ""
        self._int_dir = ""
        self._preprocessor_definitions: List[str] = []
        self.language_standard = int()
        self._additional_include_directories = ""

    @converter
    def set_out_dir(self, out_dir: str):
        self._out_dir = out_dir

    @converter
    def set_int_dir(self, int_dir: str):
        self._int_dir = int_dir

    @converter
    def add_preprocessor_definitions(self, preprocessor_definitions: str):
        if preprocessor_definitions:
            self._preprocessor_definitions.append(preprocessor_definitions)

    @converter
    def set_additional_include_directories(self, additional_include_directories: str):
        self._additional_include_directories = additional_include_directories

    def configure(self, configuration: str, sources: SourceParser, include: IncludeParser):
        self._configuration = get_vs_configuration_type_to_cmake_type(configuration) + sources.parse() + include.parse()

    def __str__(self):
        result = f"if (${{CMAKE_BUILD_TYPE}} STREQUAL {self.name})\n"

        result += Configuration._add_line(f"set(PLATFORM {self.platform})")
        result += Configuration._add_line(f"set(CONFIGURATION {self.name})")
        result += Configuration._add_line(f"set(CMAKE_CXX_STANDARD {self.language_standard})")
        result += Configuration._add_line(f"set(CMAKE_INSTALL_PREFIX {self._out_dir})", True)

        result += Configuration._add_line("add_definitions(")

        for definition in self._preprocessor_definitions:
            result += Configuration._add_line(f"\t-D{definition}")

        result += Configuration._add_line(")", True)

        result += Configuration._add_line(self._configuration, True)

        result += Configuration._add_line("install(TARGETS ${PROJECT_NAME} DESTINATION .)")

        result += "endif()"

        return result

    @staticmethod
    def _add_line(line: str, double_end_line: bool = False):
        return f"\t{line}\n\n" if double_end_line else f"\t{line}\n"
