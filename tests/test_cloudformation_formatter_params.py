import unittest
import cloudformation_formatter_params

from unittest import mock

TEMPLATE_CONFIG_FILE_JSON = {
    "Parameters": {
        "RdsDBInstanceType": "db.t2.large",
        "RdsPort": "5432",
        "RdsDBName": "test",
        "RdsUserName": "test",
        "TagName": "rds-prod",
    }
}

CLI_PARAMS_FILE_JSON = [
    {"ParameterKey": "RdsDBInstanceType", "ParameterValue": "db.t2.large"},
    {"ParameterKey": "RdsPort", "ParameterValue": "5432"},
    {"ParameterKey": "RdsDBName", "ParameterValue": "test"},
    {"ParameterKey": "RdsUserName", "ParameterValue": "test"},
    {"ParameterKey": "TagName", "ParameterValue": "rds-prod"},
]


class TestCloudformationFormatterParams(unittest.TestCase):
    @mock.patch("cloudformation_formatter_params.write_output")
    def test_main(self, write_output):

        p1 = mock.patch("builtins.open", mock.MagicMock())

        m = mock.MagicMock(side_effect=[TEMPLATE_CONFIG_FILE_JSON])
        p2 = mock.patch("json.load", m)

        with p1 as p_open:  # noqa
            with p2 as p_json_load:  # noqa
                cloudformation_formatter_params.main(
                    ["cli_params_file", "output_location.json"]
                )
                write_output.assert_called_with(
                    CLI_PARAMS_FILE_JSON, "output_location.json"
                )

        m.side_effect = [CLI_PARAMS_FILE_JSON]
        p2 = mock.patch("json.load", m)

        with p1 as p_open:  # noqa
            with p2 as p_json_load:  # noqa
                cloudformation_formatter_params.main(
                    ["cli_params_file", "output_location.json"]
                )
                write_output.assert_called_with(
                    TEMPLATE_CONFIG_FILE_JSON, "output_location.json"
                )

    def test_convert_template_config_to_cli(self):
        output = cloudformation_formatter_params.convert_template_config_to_cli(
            TEMPLATE_CONFIG_FILE_JSON
        )
        self.assertEqual(output, CLI_PARAMS_FILE_JSON)

    def test_convert_cli_to_template_config(self):
        output = cloudformation_formatter_params.convert_cli_to_template_config(
            CLI_PARAMS_FILE_JSON
        )
        self.assertEqual(output, TEMPLATE_CONFIG_FILE_JSON)


if __name__ == "__main__":
    unittest.main()
