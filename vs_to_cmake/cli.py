import argparse
import os
import pathlib
from typing import List

import xmltodict
from tqdm import tqdm

from vs_to_cmake.meta_information_parsers import VCXProjParser, ProjectParser, ReferencesParser


def parse_sln(sln_path: str, output_path: str, cmake_version: str):
    pass


def parse_vcxproj(vcxproj_path: str, file_path: str, cmake_version: str, definitions: List[str]):
    with open(vcxproj_path, "r") as xml_file:
        data = xmltodict.parse(xml_file.read())

        project_name_parser = ProjectParser(data)
        references_parser = ReferencesParser(data)
        project_parser = VCXProjParser(data, definitions)

        with open(f"{file_path}/CMakeLists.txt", "w") as file:
            file.write(f"cmake_minimum_required(VERSION {cmake_version})\n\n")

            file.write(project_name_parser.parse())

            references = references_parser.parse()

            if references:
                file.write(references)

            file.write(project_parser.parse())


def main():
    parser = argparse.ArgumentParser(
        "vs_to_cmake"
    )

    parser.add_argument("-f", "--file_path", required=True)
    parser.add_argument("-o", "--output_path", default=".")
    parser.add_argument("-v", "--cmake_version", default="3.27.0")
    parser.add_argument("-d", "--definitions", nargs='+', default=[])

    args = parser.parse_args()
    file_path = args.file_path
    output_path = args.output_path
    cmake_version = args.cmake_version
    definitions = args.definitions

    if not os.path.exists(file_path):
        raise FileExistsError(file_path)

    if pathlib.Path(os.path.split(file_path)[-1]).suffix == ".sln":
        parse_sln(file_path, output_path, cmake_version)
    elif pathlib.Path(os.path.split(file_path)[-1]).suffix == ".vcxproj":
        parse_vcxproj(file_path, output_path, cmake_version, definitions)
    else:
        raise Exception("Wrong file")


if __name__ == '__main__':
    main()
