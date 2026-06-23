import sys
import os
import tempfile
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import load_weather_file


def write_temp_file(text):
    temp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".txt", delete=False
    )

    try:
        temp.write(text)
        return temp.name
    finally:
        temp.close()


def test_load_weather_file_accepts_decimals_and_blank_lines():
    print("Running test: load_weather_file_accepts_decimals_and_blank_lines...")

    path = write_temp_file("12.5\n\n14.1\n")

    try:
        assert load_weather_file(path) == [12.5, 14.1]
    finally:
        Path(path).unlink(missing_ok=True)

    print("Test PASSED: Decimal values load and blank lines are ignored")


def test_load_weather_file_reports_bad_text():
    print("\nRunning test: load_weather_file_reports_bad_text...")

    path = write_temp_file("12.5\nabc\n14.1\n")

    try:
        try:
            load_weather_file(path)
            assert False
        except ValueError as error:
            message = str(error)
            assert Path(path).name in message
            assert "line 2" in message
            assert "not numeric" in message
    finally:
        Path(path).unlink(missing_ok=True)

    print("Test PASSED: Bad text reports file name and line number..")


def test_load_weather_file_empty_file():
    print("\nRunning test: load_weather_file_empty_file...")

    path = write_temp_file("")

    try:
        assert load_weather_file(path) == []
    finally:
        Path(path).unlink(missing_ok=True)

    print("Test PASSED: Empty file returns an empty list")


if __name__ == "__main__":
    test_load_weather_file_accepts_decimals_and_blank_lines()
    test_load_weather_file_reports_bad_text()
    test_load_weather_file_empty_file()
    print("\nAll main file tests completed successfully!!")
