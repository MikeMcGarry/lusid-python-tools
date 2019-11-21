import unittest
from pathlib import Path
import pandas as pd
import lusid
from lusidtools import cocoon as cocoon
from parameterized import parameterized
from lusidtools import logger


class CocoonTestsFailures(unittest.TestCase):
    api_factory = None

    @classmethod
    def setUpClass(cls) -> None:
        secrets_file = Path(__file__).parent.parent.parent.joinpath("secrets.json")
        cls.api_factory = lusid.utilities.ApiClientFactory(
            api_secrets_filename=secrets_file
        )
        cls.logger = logger.LusidLogger("debug")

    @parameterized.expand(
        [
            [
                "A file with a missing unique identifier for an instrument",
                "TestScope1",
                "data/global-fund-combined-instrument-master-missing-identifiers.csv",
                {"name": "instrument_name"},
                {},
                {"Figi": "figi", "Isin": "isin", "ClientInternal": "client_internal"},
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "No identifiers specified in the identifier mapping",
                "TestScope1",
                "data/global-fund-combined-instrument-master.csv",
                {"name": "instrument_name"},
                {},
                {},
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "Another way of missing the identifier mapping",
                "TestScope1",
                "data/global-fund-combined-instrument-master.csv",
                {"name": "instrument_name"},
                {},
                None,
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "A missing required attribute in the required mapping",
                "TestScope1",
                "data/global-fund-combined-instrument-master.csv",
                {},
                {},
                {"Figi": "figi", "Isin": "isin", "ClientInternal": "client_internal"},
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "None provided for the required mapping",
                "TestScope1",
                "data/global-fund-combined-instrument-master.csv",
                None,
                {},
                {"Figi": "figi", "Isin": "isin", "ClientInternal": "client_internal"},
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                TypeError,
            ],
            [
                "A file with missing names for two instruments",
                "TestScope1",
                "data/global-fund-combined-instrument-master-missing-names.csv",
                {"name": "instrument_name"},
                {},
                {"Figi": "figi", "Isin": "isin", "ClientInternal": "client_internal"},
                ["s&p rating", "moodys_rating", "currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "A property column list that contains a property not in the dataframe",
                "TestScope1",
                "data/global-fund-combined-instrument-master-missing-identifiers.csv",
                {"name": "instrument_name"},
                {},
                {"Figi": "figi", "Isin": "isin", "ClientInternal": "client_internal"},
                ["s&p rating", "moodys_rating", "currency", "transaction_currency"],
                "TestPropertiesScope1",
                "instruments",
                ValueError,
            ],
            [
                "Non unique portfolios in the file",
                "prime_broker_test",
                "data/metamorph_portfolios.csv",
                {
                    "code": "FundCode",
                    "display_name": "display_name",
                    "created": "created",
                    "base_currency": "base_currency",
                },
                {"description": "description", "accounting_method": None},
                {},
                ["base_currency"],
                "operations001",
                "portfolios",
                ValueError,
            ],
            [
                "Misnamed required parameter effective_date rather than effective_at",
                "prime_broker_test",
                "data/holdings-example-unique-date.csv",
                {
                    "code": "FundCode",
                    "effective_date": "Effective Date",
                    "tax_lots.units": "Quantity",
                },
                {
                    "tax_lots.cost.amount": None,
                    "tax_lots.cost.currency": "Local Currency Code",
                    "tax_lots.portfolio_cost": None,
                    "tax_lots.price": None,
                    "tax_lots.purchase_date": None,
                    "tax_lots.settlement_date": None,
                },
                {
                    "Isin": "ISIN Security Identifier",
                    "Sedol": "SEDOL Security Identifier",
                    "Currency": "is_cash_with_currency",
                },
                ["Prime Broker"],
                "operations001",
                "holdings",
                ValueError,
            ],
            [
                "Duplication of transaction ids",
                "prime_broker_test",
                "data/global-fund-combined-transactions-duplicate-id.csv",
                {
                    "code": "portfolio_code",
                    "transaction_id": "id",
                    "type": "transaction_type",
                    "transaction_date": "transaction_date",
                    "settlement_date": "settlement_date",
                    "units": "units",
                    "transaction_price.price": "transaction_price",
                    "transaction_price.type": "price_type",
                    "total_consideration.amount": "amount",
                    "total_consideration.currency": "trade_currency",
                },
                {"transaction_currency": "trade_currency"},
                {
                    "Isin": "isin",
                    "Figi": "figi",
                    "ClientInternal": "client_internal",
                    "Currency": "currency_transaction",
                },
                ["exposure_counterparty", "compls", "val", "location_region"],
                "operations001",
                "transaction",
                ValueError,
            ],
            [
                "Missing portfolio code",
                "prime_broker_test",
                "data/holdings-example-unique-date.csv",
                {"effective_at": "Effective Date", "tax_lots.units": "Quantity"},
                {
                    "tax_lots.cost.amount": None,
                    "tax_lots.cost.currency": "Local Currency Code",
                    "tax_lots.portfolio_cost": None,
                    "tax_lots.price": None,
                    "tax_lots.purchase_date": None,
                    "tax_lots.settlement_date": None,
                },
                {
                    "Isin": "ISIN Security Identifier",
                    "Sedol": "SEDOL Security Identifier",
                    "Currency": "is_cash_with_currency",
                },
                ["Prime Broker"],
                "operations001",
                "holdings",
                ValueError,
            ],
            [
                "A file type that is not supported",
                "prime_broker_test",
                "data/holdings-example-unique-date.csv",
                {
                    "effective_at": "Effective Date",
                    "code": "Account Id",
                    "tax_lots.units": "Quantity",
                },
                {
                    "tax_lots.cost.amount": None,
                    "tax_lots.cost.currency": "Local Currency Code",
                    "tax_lots.portfolio_cost": None,
                    "tax_lots.price": None,
                    "tax_lots.purchase_date": None,
                    "tax_lots.settlement_date": None,
                },
                {
                    "Isin": "ISIN Security Identifier",
                    "Sedol": "SEDOL Security Identifier",
                    "Currency": "is_cash_with_currency",
                },
                ["Prime Broker"],
                "operations001",
                "reference",
                ValueError,
            ],
        ]
    )
    def test_load_from_data_frame_failure(
        self,
        test_name,
        scope,
        file_name,
        mapping_required,
        mapping_optional,
        identifier_mapping,
        property_columns,
        properties_scope,
        file_type,
        expected_exception,
    ) -> None:
        """
        Test for failure cases

        :param str scope: The scope of the portfolios to load the transactions into
        :param str file_name: The name of the test data file
        :param dict{str, str} mapping_required: The dictionary mapping the dataframe fields to LUSID's required base transaction/holding schema
        :param dict{str, str} mapping_optional: The dictionary mapping the dataframe fields to LUSID's optional base transaction/holding schema
        :param dict{str, str} identifier_mapping: The dictionary mapping of LUSID instrument identifiers to identifiers in the dataframe
        :param list[str] property_columns: The columns to create properties for
        :param str properties_scope: The scope to add the properties to
        :param str file_type: The file type to load
        :param any expected_exception: The expected exception

        :return: None
        """
        # ignore tests
        ignore = ["Non unique portfolios in the file", "Duplication of transaction ids"]

        if test_name in ignore:
            self.skipTest("not yet implemented")

        data_frame = pd.read_csv(Path(__file__).parent.joinpath(file_name))

        with self.assertRaises(expected_exception):

            cocoon.cocoon.load_from_data_frame(
                api_factory=self.api_factory,
                scope=scope,
                data_frame=data_frame,
                mapping_required=mapping_required,
                mapping_optional=mapping_optional,
                file_type=file_type,
                identifier_mapping=identifier_mapping,
                property_columns=property_columns,
                properties_scope=properties_scope,
            )