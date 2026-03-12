"""
Exam 1 - Test Inventory Module
================================
Write your tests below. Each section (Part A through E) is marked.
Follow the instructions in each part carefully.

Run your tests with:
    pytest test_inventory.py -v

Run with coverage:
    pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
"""

import pytest
from unittest.mock import patch
from inventory import (
    add_product,
    get_product,
    update_stock,
    calculate_total,
    apply_bulk_discount,
    list_products,
)
from inventory import get_low_stock_products  # Bonus

# ============================================================
# FIXTURE: Temporary inventory file (provided for you)
# This ensures each test gets a clean, isolated inventory.
# ============================================================


@pytest.fixture(autouse=True)
def clean_inventory(tmp_path, monkeypatch):
    """Use a temporary inventory file for each test."""
    db_file = str(tmp_path / "inventory.json")
    monkeypatch.setattr("inventory.INVENTORY_FILE", db_file)
    yield


# ============================================================
# PART A - Basic Assertions (18 marks)
# Write at least 8 tests using plain assert statements.
# Cover: add_product, get_product, update_stock,
#        calculate_total, and list_products.
# Follow the AAA pattern (Arrange, Act, Assert).
# ============================================================

# TODO: Write your Part A tests here


# 1
def test_add_product():
    # Arrange & Act
    product = add_product("P001", "Laptop", 300, 10)

    # Assert
    assert product["product_id"] == "P001"
    assert product["name"] == "Laptop"
    assert product["price"] == 300
    assert product["stock"] == 10


# 2
def test_get_product_existing():
    # Arrange
    add_product("P001", "Laptop", 300, 10)

    # Act
    product = get_product("P001")

    # Assert
    assert product["product_id"] == "P001"
    assert product["name"] == "Laptop"
    assert product["price"] == 300
    assert product["stock"] == 10


# 3
def test_get_product_not_found():
    # Arrange & Act
    product = get_product("P999")

    # Assert
    assert product is None


# 4
def test_update_stock_increase():
    # Arrange
    add_product("P001", "Laptop", 300, 20)

    # Act
    new_stock = update_stock("P001", 5)

    # Assert
    assert new_stock == 25


# 5
def test_update_stock_decrease():
    # Arrange
    add_product("P001", "Laptop", 300, 20)

    # Act
    new_stock = update_stock("P001", -10)

    # Assert
    assert new_stock == 10


# 6
def test_calculate_total():
    # Arrange
    add_product("P001", "Mouse", 9.99, 50)

    # Act
    total = calculate_total("P001", 3)

    # Assert
    assert total == 29.97


# 7
def test_list_products_count():
    # Arrange
    add_product("P001", "Laptop", 300, 10)
    add_product("P002", "Mouse", 20, 50)

    # Act
    products = list_products()

    # Assert
    assert len(products) == 2


# 8
def test_list_products_content():
    # Arrange
    add_product("P001", "Laptop", 300, 10)

    # Act
    products = list_products()

    # Assert
    assert products[0]["product_id"] == "P001"


# ============================================================
# PART B - Exception Testing (12 marks)
# Write at least 6 tests using pytest.raises.
# Cover: empty name, negative price, duplicate product,
#        stock going below zero, product not found, etc.
# ============================================================

# TODO: Write your Part B tests here


# 1
def test_add_product_empty_id():
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product("", "Laptop", 300, 10)


# 2
def test_add_product_empty_name():
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product("P001", "", 300, 10)


# 3
def test_add_product_negative_price():
    with pytest.raises(ValueError, match="Price must be positive"):
        add_product("P001", "Laptop", -5, 10)


# 4
def test_add_product_duplicate():
    add_product("P001", "Laptop", 300, 10)

    with pytest.raises(ValueError, match="already exists"):
        add_product("P001", "Laptop", 300, 10)


# 5
def test_update_stock_below_zero():
    add_product("P001", "Laptop", 300, 5)

    with pytest.raises(ValueError, match="Stock cannot go below zero"):
        update_stock("P001", -10)


# 6
def test_calculate_total_invalid_quantity():
    add_product("P001", "Laptop", 300, 5)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        calculate_total("P001", 0)


# [Added] to raise coverage to be more than 91%
def test_apply_bulk_discount_negative_quantity():
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        apply_bulk_discount(100, -1)


# [Added] to raise coverage to be more than 91%
def test_apply_bulk_discount_negative_total():
    with pytest.raises(ValueError, match="Total cannot be negative"):
        apply_bulk_discount(-100, 5)


# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
#
# C1: Create a @pytest.fixture called "sample_products" that
#     adds 3 products to the inventory and returns their IDs.
#     Write 2 tests that use this fixture.
#
# C2: Use @pytest.mark.parametrize to test apply_bulk_discount
#     with at least 5 different (total, quantity, expected) combos.
# ============================================================

# TODO: Write your Part C tests here


# C1
@pytest.fixture
def sample_products():
    add_product("P001", "Laptop", 999.99, 10)
    add_product("P002", "Mouse", 29.99, 50)
    add_product("P003", "Keyboard", 79.99, 25)

    return ["P001", "P002", "P003"]


def test_fixture_list_products(sample_products):
    # Act
    products = list_products()

    # Assert
    assert len(products) == 3


def test_fixture_calculate_total(sample_products):
    # Act
    total = calculate_total("P002", 2)

    # Assert
    assert total == 59.98


# C2
@pytest.mark.parametrize(
    "total,quantity,expected",
    [
        (100, 5, 100),  # no discount
        (100, 10, 95),  # 5%
        (100, 25, 90),  # 10%
        (100, 50, 85),  # 15%
        (200, 30, 180),  # 10%
    ],
)
def test_apply_bulk_discount(total, quantity, expected):
    result = apply_bulk_discount(total, quantity)
    assert result == expected


# ============================================================
# PART D - Mocking (5 marks)
# Use @patch to mock _send_restock_alert.
# Write 2 tests:
#   1. Verify the alert IS called when stock drops below 5
#   2. Verify the alert is NOT called when stock stays >= 5
# ============================================================


# TODO: Write your Part D tests here


#   1. Verify the alert IS called when stock drops below 5
@patch("inventory._send_restock_alert")
def test_restock_alert_called(mock_alert):
    # Arrange
    add_product("P001", "Laptop", 300, 6)

    # Act
    update_stock("P001", -3)

    # Assert
    mock_alert.assert_called_once_with("P001", "Laptop", 3)


#   2. Verify the alert is NOT called when stock stays >= 5
@patch("inventory._send_restock_alert")
def test_restock_alert_not_called(mock_alert):
    # Arrange
    add_product("P001", "Laptop", 300, 20)

    # Act
    update_stock("P001", -5)

    # Assert
    mock_alert.assert_not_called()


# [Added] to ensure that no alert is sent when stock is 5
@patch("inventory._send_restock_alert")
def test_restock_alert_stock_exactly_five(mock_alert):
    add_product("P003", "Keyboard", 50, 8)
    update_stock("P003", -3)
    mock_alert.assert_not_called()


# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# You must achieve 90%+ coverage on inventory.py.
# If lines are missed, add more tests above to cover them.
# ============================================================


# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================

# TODO: Write your bonus tests here (optional)


@pytest.mark.parametrize(
    "threshold,expected",
    [
        (5, 0),
        (50, 2),
        (0, 0),
    ],
)
def test_get_low_stock_products(sample_products, threshold, expected):
    result = get_low_stock_products(threshold)
    assert len(result) == expected
