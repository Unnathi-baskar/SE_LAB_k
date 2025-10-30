"""
Inventory Management System

This module provides functions to manage a simple in-memory inventory system.
It allows adding, removing, saving, and loading item data, as well as checking
for low stock. All data is stored in a dictionary and can be persisted to a
JSON file.
"""

import json
from datetime import datetime


def add_item(item="default", qty=0, logs=None, stock_data=None):
    """
    Adds an item and quantity to the inventory.

    Args:
        item (str): Name of the item.
        qty (int): Quantity to add (must be positive).
        logs (list, optional): List to store operation logs.
        stock_data (dict, optional): The inventory dictionary.
    """
    if logs is None:
        logs = []
    if stock_data is None:
        stock_data = {}

    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid input types. Item must be string, qty must be integer.")
        return

    if qty < 0:
        print("Cannot add negative quantity.")
        return

    if not item:
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty, stock_data):
    """
    Removes a quantity of an item from the inventory.

    Args:
        item (str): Item name to remove.
        qty (int): Quantity to remove.
        stock_data (dict): The inventory dictionary.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Item '{item}' not found in inventory.")
    except (TypeError, ValueError) as e:
        print(f"Invalid quantity or data type: {e}")


def get_qty(item, stock_data):
    """
    Returns the quantity available for a given item.

    Args:
        item (str): Item name.
        stock_data (dict): The inventory dictionary.

    Returns:
        int: Quantity in stock.
    """
    return stock_data.get(item, 0)


def load_data(file_path="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        file_path (str): Path to the inventory file.

    Returns:
        dict: The loaded inventory data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No existing inventory file found. Starting fresh.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding inventory file. Starting fresh.")
        return {}


def save_data(stock_data, file_path="inventory.json"):
    """
    Saves current inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary.
        file_path (str): Path to the file where data will be saved.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(stock_data, file, indent=4)
    except (OSError, IOError) as e:
        print(f"Error saving data: {e}")


def print_data(stock_data):
    """
    Prints all items and their quantities.
    """
    print("\nItems Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(stock_data, threshold=5):
    """
    Checks for items below the given threshold quantity.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): Minimum quantity limit.

    Returns:
        list: Items below the threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to demonstrate inventory operations.
    """
    stock_data = {}

    add_item("apple", 10, stock_data=stock_data)
    add_item("banana", -2, stock_data=stock_data)
    add_item(123, "ten", stock_data=stock_data)

    remove_item("apple", 3, stock_data)
    remove_item("orange", 1, stock_data)

    print("Apple stock:", get_qty("apple", stock_data))
    print("Low items:", check_low_items(stock_data))

    save_data(stock_data)
    stock_data = load_data()
    print_data(stock_data)

    code_string = '{"action": "print used"}'
    try:
        parsed_data = json.loads(code_string)
        print(parsed_data)
    except json.JSONDecodeError as e:
        print("Invalid JSON input:", e)


if __name__ == "__main__":
    main()
