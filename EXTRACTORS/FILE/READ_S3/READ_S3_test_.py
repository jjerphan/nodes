import pytest
from unittest.mock import patch
import io
import boto3
import moto
import pandas as pd
from flojoy import DataFrame


# Test dataframe to write as parquet file
@pytest.fixture
def test_dataframe():
    return pd.DataFrame.from_dict({"a": [1, 2, 3], "b": [4, 5, 6]})


# This creates a fake bucket under s3://test_bucket with a file under s3://test_bucket/test_df.parquet
@pytest.fixture
def mock_bucket(test_dataframe):
    with moto.mock_s3() as moto_fake:
        conn = boto3.resource("s3")
        conn.create_bucket(Bucket="test_bucket")
        test_bucket = conn.Bucket("test_bucket")
        # Write a parquet file to the bucket
        with io.BytesIO() as f:
            test_dataframe.to_parquet(f)
            test_bucket.put_object(Key="test_df.parquet", Body=f.getvalue())
        yield conn


# Mock keyring to return None
@pytest.fixture
def mock_keyring_get_password():
    # Mock keyring get_password et
    with patch("keyring.get_password", return_value=None) as mock_keyright:
        yield mock_keyright


def test_READ_S3(
    mock_flojoy_decorator,
    mock_bucket,
    mock_keyring_get_password,
    test_dataframe,
):
    import READ_S3

    output = READ_S3.READ_S3("test", "test_bucket", "test_df.parquet")
    assert output.m.equals(test_dataframe)
