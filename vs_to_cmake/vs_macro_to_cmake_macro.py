_macros = {
    "$(SolutionDir)": "${CMAKE_SOURCE_DIR}/",
    "$(Configuration)": "${VS_CONFIGURATION}",
    "$(ProjectDir)": "${PROJECT_SOURCE_DIR}/",
    "$(Platform)": "${VS_PLATFORM}",
    "$(ProjectName)": "${PROJECT_NAME}",
    "%(PreprocessorDefinitions)": ""
}

_configuration_type = {
    "DynamicLibrary": "add_library(\n\t\t${PROJECT_NAME} SHARED\n",
    "StaticLibrary": "add_library(\n\t\t${PROJECT_NAME} STATIC\n",
    "Application": "add_executable(\n\t\t${PROJECT_NAME}\n"
}


def converter(func):
    def wrapper(*args, **kwargs):
        data = str(args[1]).replace('\\', '/')

        for key, value in _macros.items():
            if key in data:
                data = data.replace(key, value)

        new_args = (args[0], data)

        func(*new_args, **kwargs)

    return wrapper


def get_vs_configuration_type_to_cmake_type(configuration_type: str) -> str:
    return _configuration_type[configuration_type]
