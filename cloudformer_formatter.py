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

def main():
    parser = argparse.ArgumentParser(description='CloudFormer formatter - Tool to improve on default CloudFormer resourcenames ')
    parser.add_argument('input', type=str, nargs='?',
                        help='Input JSON file ')
    parser.add_argument('output', type=str, nargs='?',
                        help='Formatted output JSON file')
    args = parser.parse_args()

    with open(args.input, 'r') as input_file:
        json_data = json.load(input_file)
        for resource_name in json_data['Resources']:
            resource_type = json_data['Resources'][resource_name]['Type']

            # use resource type for new name; append counter for multiple occurences of same type
            new_name = resource_type[resource_type.rfind(':')+1:]
            process_name(resource_name, new_name)

        for resource_name, new_name in replacements.items():
            json_data['Resources'][new_name] = json_data['Resources'].pop(resource_name)

        replace_references(json_data)

        with open(args.output, 'w') as output_file:
            json.dump(json_data, output_file, indent=2)

def process_name(resource_name, new_name):
    if not new_name in processed_resources:
        processed_resources[new_name] = 1
    else:
        processed_resources[new_name] += 1
        new_name = new_name + str(processed_resources[new_name])
    replacements[resource_name] = new_name;

def replace_references(d):
    for k, v in d.items():
        if isinstance(v, dict):
            v = replace_references(v)
        if(k == 'Ref'):
            d['Ref'] = replacements[v]

if __name__ == '__main__':
    main()
