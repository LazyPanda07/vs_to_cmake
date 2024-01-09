import argparse
import os
import pathlib

import xmltodict
from tqdm import tqdm

from vs_to_cmake.parsers import SourceParser, ProjectParser, IncludeParser, CXXStandardParser


def parse_sln(sln_path: str, output_path: str, cmake_version: str):
    pass


def parse_vcxproj(vcxproj_path: str, output_path: str, cmake_version: str):
    with open(vcxproj_path, "r") as xml_file:
        data = xmltodict.parse(xml_file.read())

        project_name = ProjectParser(data)
        cxx_standard = CXXStandardParser(data)
        sources = SourceParser(data)
        include = IncludeParser(data)

        with open(f"{output_path}/CMakeLists.txt", "w") as file:
            file.write(f"cmake_minimum_required(VERSION {cmake_version})\n\n")

            file.write(project_name.parse())

            file.write(cxx_standard.parse())

            file.write(sources.parse())

            file.write(include.parse())


def main():
    parser = argparse.ArgumentParser(
        "vs_to_cmake"
    )

    parser.add_argument("--path_to_file", required=True)
    parser.add_argument("--output_path", default=".")
    parser.add_argument("--cmake_version", default="3.27.0")
    # parser.add_argument("--clean", action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()
    path_to_file = args.path_to_file
    output_path = args.output_path
    cmake_version = args.cmake_version

    if not os.path.exists(path_to_file):
        raise FileExistsError(path_to_file)

    if pathlib.Path(os.path.split(path_to_file)[-1]).suffix == ".sln":
        parse_sln(path_to_file, output_path, cmake_version)
    elif pathlib.Path(os.path.split(path_to_file)[-1]).suffix == ".vcxproj":
        parse_vcxproj(path_to_file, output_path, cmake_version)


if __name__ == '__main__':
    main()
