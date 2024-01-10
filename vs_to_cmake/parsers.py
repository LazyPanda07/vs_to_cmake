from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, data: dict):
        self._data = data

    @abstractmethod
    def parse(self) -> str:
        pass


class CXXStandardParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        cxx = str(self._data['Project']['ItemDefinitionGroup'][0]['ClCompile']['LanguageStandard'])
        cxx = cxx.replace("stdcpp", "")
        return f"set(CMAKE_CXX_STANDARD {cxx})\n\n"


class SourceParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        result = "add_library(\n" + "\t${PROJECT_NAME} STATIC\n"

        for i in self._data["Project"]["ItemGroup"]:
            if "ClCompile" in i:
                for j in i["ClCompile"]:
                    result += f"\t{j['@Include']}\n".replace("\\", "/")

        result += ")\n\n"

        return result


class ProjectParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        for i in self._data["Project"]["PropertyGroup"]:
            if "RootNamespace" in i:
                return f"project({i['RootNamespace']})\n\n"


class IncludeParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)

    def parse(self) -> str:
        result = "target_include_directories(\n" + "\t${PROJECT_NAME} PRIVATE\n"
        includes = str(self._data["Project"]["ItemDefinitionGroup"][0]["ClCompile"]["AdditionalIncludeDirectories"]).split(';')

        for include in includes:
            include = include.replace("$(ProjectDir)", "${PROJECT_SOURCE_DIR}/")
            result += f"\t{include}\n".replace("\\", "/")

        result += ")\n"

        return result
