from vs_to_cmake.base_parser import BaseParser


class SourceParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        result = ""

        for i in self._data["Project"]["ItemGroup"]:
            if "ClCompile" in i:
                for j in i["ClCompile"]:
                    result += f"\t\t{j['@Include']}\n".replace("\\", "/")

        result += "\t)\n\n"

        return result


class IncludeParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        if "AdditionalIncludeDirectories" not in self._data["Project"]["ItemDefinitionGroup"][0]["ClCompile"]:
            return ""

        result = "\ttarget_include_directories(\n" + "\t\t${PROJECT_NAME} PUBLIC\n"
        includes = str(
            self._data["Project"]["ItemDefinitionGroup"][0]["ClCompile"]["AdditionalIncludeDirectories"]).split(';')

        for include in includes:
            include = include.replace("$(ProjectDir)", "${PROJECT_SOURCE_DIR}/")
            result += f"\t\t{include}\n".replace("\\", "/")

        result += "\t)"

        return result
