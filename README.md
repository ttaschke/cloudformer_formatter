# CloudFormer Formatter

> Tool to improve on default CloudFormer resourcenames

AWS provides the CloudFormer tool (https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html) to enable users to create CloudFormation templates from existing AWS resources.
In the resulting template all resourcenames are set to the resource id, which in most cases is a meaningless random generated id. It is left to the user to manually change the resourcenames to more meaningful names.
As the generated templates can be quite big and contain hundreds of resources this unfortunately takes a significan amount of time. Cloudformer Formatter solves this problem by automatically replacing these default generated resourcenames with more meaningful names that are based on the resource type name.

* Release 1.0.0
* Python 3.6.5

## Usage
```
usage: python cloudformer_formatter.py [-h] [input] [output]

CloudFormer formatter - Tool to improve on default CloudFormer resourcenames

positional arguments:
  input       Input JSON file
  output      Formatted output JSON file

optional arguments:
  -h, --help  show this help message and exit
```

### Example

Default output of CloudFormer tool:

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "vpcb9bcc3cb": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
        ...
      }
    },
    "vpcb545fcb": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
        ...
      }
    },
    "subnet502ab36f": {
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        ...
        "VpcId": {
          "Ref": "vpcb9bcc3cb"
        }
      }
    }
  }
}

```

Converted output from CloudFormer formatter:
```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "VPC": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
        ...
      }
    },
    "VPC2": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
        ...
      }
    },
    "Subnet": {
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        ...
        "VpcId": {
          "Ref": "VPC"
        }
      }
    }
  }
}
```