import re

from base_parser import BaseParser
from source_parsers import SourceParser, IncludeParser
from configuration import Configuration


class VCXProjParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

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
                        configuration.set_int_dir(property_group["IntDir"])

            for item_definition_group in self._data["Project"]["ItemDefinitionGroup"]:
                if f"'$(Configuration)|$(Platform)'=='{name}|{platform}'" == item_definition_group["@Condition"]:
                    information = item_definition_group["ClCompile"]
                    definitions = information["PreprocessorDefinitions"].split(';')

                    for definition in definitions:
                        configuration.add_preprocessor_definitions(definition)

                    configuration.language_standard = int(re.search(r"\d+", information["LanguageStandard"]).group())
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
