#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json

"""
CloudFormer formatter resourcenames - Tool to improve on default CloudFormer resourcenames

Replaces the default generated resourcenames that AWS' CloudFormer tool (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html)
outputs with more meaningful names that are based on the resource type
"""

processed_resources = {}
replacements = {}


def main(args_cli):
    parser = argparse.ArgumentParser(
        description="CloudFormer formatter - Tool to improve on default CloudFormer resourcenames"
    )
    parser.add_argument("input", type=str, nargs="?", help="Input JSON file ")
    parser.add_argument(
        "output", type=str, nargs="?", help="Formatted output JSON file"
    )
    args = parser.parse_args(args_cli)

    with open(args.input, "r") as input_file:
        json_data = json.load(input_file)
        for resource_name in json_data["Resources"]:
            resource_type = json_data["Resources"][resource_name]["Type"]

            # use resource type for new name; append counter for multiple occurences of same type
            new_name = resource_type[resource_type.rfind(":") + 1 :]  # noqa
            process_resource_name(resource_name, new_name)

        for resource_name, new_name in replacements.items():
            json_data["Resources"][new_name] = json_data["Resources"].pop(resource_name)

        replace_references(json_data)

    write_output(json_data, args.output)


def process_resource_name(resource_name, new_name):
    if new_name not in processed_resources:
        processed_resources[new_name] = 1
    else:
        processed_resources[new_name] += 1
        new_name = new_name + str(processed_resources[new_name])
    replacements[resource_name] = new_name


def replace_references(json_data):
    for k, v in json_data.items():
        if isinstance(v, dict):
            v = replace_references(v)
        if k == "Ref":
            json_data["Ref"] = replacements[v]


def write_output(output, output_location):
    with open(output_location, "w") as output_file:
        json.dump(output, output_file, indent=2)


if __name__ == "__main__":
    main()
