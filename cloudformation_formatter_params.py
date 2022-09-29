#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json


"""
CloudFormer formatter Params- Tool to convert files between different formats used to set parameters for Cloudformation.

This tool converts between the JSON file used to define parameters when creating a stack using the AWS CLI and
a Template Configuration JSON File used by CodePipeline to set the parameters of a stack.
The format will be detected automatically and converted into the appropriate output format.
"""


def main(args_cli):
    parser = argparse.ArgumentParser(
        description="CloudFormer formatter - Tool to convert files between different formats used to set parameters for Cloudformation"
    )
    parser.add_argument("input", type=str, nargs="?", help="Input JSON file ")
    parser.add_argument(
        "output", type=str, nargs="?", help="Formatted output JSON file"
    )
    args = parser.parse_args(args_cli)

    with open(args.input, "r") as input_file:

        json_data = json.load(input_file)

        if isinstance(
            json_data, dict
        ):  # the file is a dict, thus a template configuration file
            output = convert_template_config_to_cli(json_data)
        else:  # the file is an AWS CLI param file
            output = convert_cli_to_template_config(json_data)

    write_output(output, args.output)


def convert_template_config_to_cli(json_data):
    params = []

    for param_key, param_value in json_data["Parameters"].items():
        params.append({"ParameterKey": param_key, "ParameterValue": param_value})
    return params


def convert_cli_to_template_config(json_data):

    output = {}
    output["Parameters"] = {}

    for param_pair in json_data:
        output["Parameters"][param_pair["ParameterKey"]] = param_pair["ParameterValue"]

    return output


def write_output(output, output_location):
    with open(output_location, "w") as output_file:
        json.dump(output, output_file, indent=2)


if __name__ == "__main__":
    main()
