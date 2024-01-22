import re
from typing import List

from vs_to_cmake.base_parser import BaseParser
from vs_to_cmake.source_parsers import SourceParser, IncludeParser
from vs_to_cmake.configuration import Configuration


class VCXProjParser(BaseParser):
    _latest_cpp_standard = 20

    def __init__(self, data: dict, definitions: List[str]):
        super().__init__(data)

        self._definitions = definitions

    def parse(self) -> str:
        result = ""
        configurations = []
        item_group = []

        for i in self._data["Project"]["ItemGroup"]:
            if "@Label" in i:
                item_group = i["ProjectConfiguration"]
                break

        for configuration in item_group:
            configurations.append(Configuration(configuration["Configuration"], configuration["Platform"]))

        for configuration in configurations:
            name, platform = configuration.name, configuration.platform
            for property_group in self._data["Project"]["PropertyGroup"]:
                if ("@Condition" in property_group and
                        f"'$(Configuration)|$(Platform)'=='{name}|{platform}'" == property_group["@Condition"]):
                    if "ConfigurationType" in property_group:
                        configuration.configure(
                            property_group["ConfigurationType"], SourceParser(self._data), IncludeParser(self._data)
                        )
                    else:
                        configuration.set_out_dir(property_group["OutDir"])

            for item_definition_group in self._data["Project"]["ItemDefinitionGroup"]:
                if f"'$(Configuration)|$(Platform)'=='{name}|{platform}'" == item_definition_group["@Condition"]:
                    information = item_definition_group["ClCompile"]
                    definitions = information["PreprocessorDefinitions"].split(';')

                    for definition in definitions:
                        configuration.add_preprocessor_definitions(definition)

                    for definition in self._definitions:
                        configuration.add_preprocessor_definitions(definition)

                    if information["LanguageStandard"] == "stdcpplatest":
                        configuration.language_standard = VCXProjParser._latest_cpp_standard
                    else:
                        configuration.language_standard = int(re.search(r"\d+", information["LanguageStandard"]).group())

                    if "AdditionalIncludeDirectories" in information:
                        configuration.set_additional_include_directories(information["AdditionalIncludeDirectories"])

        for configuration in configurations:
            result += str(configuration) + "\n\n"

        return result


class ProjectParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        for i in self._data["Project"]["PropertyGroup"]:
            if "RootNamespace" in i:
                return f"project({i['RootNamespace']})\n\n"


class ReferencesParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        result = ""

        references = None

        for i in self._data["Project"]["ItemGroup"]:
            if "ProjectReference" in i:
                references = i["ProjectReference"]
                break

        if references is None:
            return result

        link_libraries = []

        if type(references) is list:
            for reference in references:
                result += f"add_subdirectory({self._convert(reference['@Include'], link_libraries)})\n"

            result += '\n'
        else:
            result = f"add_subdirectory({self._convert(references['@Include'], link_libraries)})\n\n"

        result += "target_link_libraries(\n\t${PROJECT_NAME}\n"

        for library in link_libraries:
            result += f"\t{library}\n"

        result += ")\n\n"

        return result

    @staticmethod
    def _convert(path: str, link_libraries: List[str]) -> str:
        components = path.replace('\\', '/').split('/')

        link_libraries.append(components[-1].split('.')[0])

        del components[-1]

        return "/".join(components)
