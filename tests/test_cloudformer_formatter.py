import unittest
import cloudformer_formatter

from unittest import mock

CLOUDFORMER_OUTPUT = {
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "vpcb9bcc3cb": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
      }
    },
    "vpcb545fcb": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
      }
    },
    "subnet502ab36f": {
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        "VpcId": {
          "Ref": "vpcb9bcc3cb"
        }
      }
    }
  }
}

EXPECTED_RESULT = {
  "AWSTemplateFormatVersion": "2010-09-09",
  "Resources": {
    "VPC": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
      }
    },
    "VPC2": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
      }
    },
    "Subnet": {
      "Type": "AWS::EC2::Subnet",
      "Properties": {
        "VpcId": {
          "Ref": "VPC"
        }
      }
    }
  }
}


class TestCloudformerFormatter(unittest.TestCase):

    @mock.patch('cloudformer_formatter.write_output')
    def test_main(self, write_output):

        p1 = mock.patch("builtins.open", mock.MagicMock())

        m = mock.MagicMock(side_effect = [CLOUDFORMER_OUTPUT])
        p2 = mock.patch("json.load", m)

        with p1 as p_open:
            with p2 as p_json_load:
                cloudformer_formatter.main(['cloudformer_output','output_location.json'])
                write_output.assert_called_with(EXPECTED_RESULT,'output_location.json')

if __name__ == '__main__':
    unittest.main()
