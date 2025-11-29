# tests/test_preprocess.py
from processing.preprocess import preprocess


def test_preprocess_creates_csv(tmp_path):
    # Use tmp_path as the temporary DATA_DIR
    DATA_DIR = tmp_path

    # Create a dummy input CSV
    input_file = DATA_DIR / "raw.csv"
    input_file.write_text(
        "bank,review_id,review,rating,date,source\n"
        "CBE,1,Great app!,5,2025-11-29,Google Play\n"
        "CBE,2,Buggy app,2,2025-11-29,Google Play\n"
    )
    output_file = DATA_DIR / "clean.csv"

    df = preprocess(str(input_file), str(output_file))

    # Check the output file exists
    assert output_file.exists()

    # Check that it has the expected columns (E501 Fix)
    expected_columns = {
        "review_id",
        "review_text",
        "rating",
        "date",
        "bank",
        "source"
    }
    assert set(df.columns) == expected_columns

    # Check row count
    assert len(df) == 2

    # Optional: Check that dates are correctly formatted
    assert all(df["date"] == ["2025-11-29", "2025-11-29"])
    