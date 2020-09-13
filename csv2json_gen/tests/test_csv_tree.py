"""Unitests for testing csv_tree libraries"""

from pathlib import Path

import pytest
from csv2json_gen.csv_tree import generate_tree, level_format
from csv2json_gen.exceptions import InvalidCSVFormat
from csv2json_gen.json_generator import read_csv


def get_resource(fname):
    """Method to read CSV data from resources directory"""
    path = Path(__file__).parent.parent.absolute()
    file_name = f"{path}/resources/{fname}"
    data = read_csv(file_name)
    return data


def test_validate_headrow_1():
    """Validate if order of parsing is as per input head row"""
    head_row = [
        "Base URL",
        "Level 1 - Name",
        "Level 1 - ID",
        "Level 1 - URL",
    ]
    order = level_format(head_row)
    assert order == ["label", "id", "link"]


def test_validate_headrow_2():
    """Validate if order of parsing is as per input head row"""
    head_row = [
        "Base URL",
        "Level 1 - URL",
        "Level 1 - ID",
        "Level 1 - Name",
    ]
    order = level_format(head_row)
    assert order == ["link", "id", "label"]


def test_validate_headrow_3():
    """Validate if exception is throw on non "Level" prefixed column"""
    head_row = ["Base URL", "Name"]
    with pytest.raises(InvalidCSVFormat) as exc:
        level_format(head_row)
    assert "Column Name is not prefixed with 'Level" in str(exc.value)


def test_validate_headrow_4():
    """Validate if column heading does not match known keyword"""
    head_row = [
        "Base URL",
        "Level 1 - LABEL",
        "Level 1 - ID",
        "Level 1 - URL",
    ]
    with pytest.raises(InvalidCSVFormat) as exc:
        level_format(head_row)
    assert "Unknown Column Name" in str(exc.value)


def test_generate_tree_1():
    """Validate if two independent root trees are created"""
    order = ["label", "id", "link"]
    csv_data = get_resource("test1.csv")
    csv_data.pop(0)
    data = generate_tree(csv_data, order)
    assert len(data) == 2


def test_generate_tree_2():
    """Validate if the CSV data matches the JSON tree output"""
    order = ["label", "id", "link"]
    csv_data = get_resource("test1.csv")
    csv_data.pop(0)
    data = generate_tree(csv_data, order)
    assert data[0]["children"][0]["label"] == "BAKERY & CAKES"
