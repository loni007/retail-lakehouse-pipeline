import pandas as pd
from retail_pipeline.validation import validate_non_negative, validate_not_null, validate_unique


def test_validate_non_negative_flags_bad_values():
    df = pd.DataFrame({"quantity": [1, -2]})
    errors = validate_non_negative(df, ["quantity"])
    assert errors


def test_validate_not_null_flags_nulls():
    df = pd.DataFrame({"order_id": [1, None]})
    errors = validate_not_null(df, ["order_id"])
    assert errors


def test_validate_unique_passes_unique_values():
    df = pd.DataFrame({"customer_id": [1, 2, 3]})
    errors = validate_unique(df, ["customer_id"])
    assert errors == []
