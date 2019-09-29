import unittest
import cloudformation_formatter_params

import json
from unittest.mock import patch, MagicMock

TEMPLATE_CONFIG_FILE_JSON = {
    "Parameters" : {
        "RdsDBInstanceType"           : "db.t2.large",
        "RdsPort"                     : "5432",
        "RdsDBName"                   : "test",
        "RdsUserName"                 : "test",
        "TagName"                     : "rds-prod"
    }
}

CLI_PARAMS_FILE_JSON = [
  {
    "ParameterKey": "RdsDBInstanceType",
    "ParameterValue": "db.t2.large"
  },
  {
    "ParameterKey": "RdsPort",
    "ParameterValue": "5432"
  },
  {
    "ParameterKey": "RdsDBName",
    "ParameterValue": "test"
  },
  {
    "ParameterKey": "RdsUserName",
    "ParameterValue": "test"
  },
  {
    "ParameterKey": "TagName",
    "ParameterValue": "rds-prod"
  }
]

class TestCloudformationFormatterParams(unittest.TestCase):

    def test_main(self):
        # I don't care about the actual open
        p1 = patch( "builtins.open", MagicMock() )

        m = MagicMock( side_effect = [ TEMPLATE_CONFIG_FILE_JSON ] )
        p2 = patch( "json.load", m )

        with p1 as p_open:
            with p2 as p_json_load:
                cloudformation_formatter_params.main(['cli_params_file','output_location.json'])
                # todo


    def test_convert_template_config_to_cli(self):
        output = cloudformation_formatter_params.convert_template_config_to_cli(TEMPLATE_CONFIG_FILE_JSON)
        self.assertEqual(output, CLI_PARAMS_FILE_JSON)

    def test_convert_cli_to_template_config(self):
        output = cloudformation_formatter_params.convert_cli_to_template_config(CLI_PARAMS_FILE_JSON)
        self.assertEqual(output, TEMPLATE_CONFIG_FILE_JSON)

if __name__ == '__main__':
    unittest.main()