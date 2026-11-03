"""
CampusFind - Smart Campus Lost & Found Portal
Python OOPS Assessment Project

Run: python main.py
No external packages required.
"""

import json
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

DATA_FILE = Path(__file__).with_name("campusfind_data.json")


class User:
    """Represents a person using the campus portal."""

    def __init__(self, name, user_id):
        self.name = name.strip()
        self.user_id = user_id.strip()

    def get_details(self):
        return f"{self.name} (ID: {self.user_id})"


class Item(ABC):
    """Abstract base class shared by lost and found reports."""

    def __init__(self, item_id, name, category, location, description,
                 reporter, date_reported=None, status="Open"):
        self.__item_id = item_id
        self.__name = name.strip()
        self.__category = category.strip().lower()
        self.__location = location.strip()
        self.__description = description.strip()
        self.reporter = reporter
        self.date_reported = date_reported or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.status = status

    @property
    def item_id(self):
        return self.__item_id

    @property
    def name(self):
        return self.__name

    @property
    def category(self):
        return self.__category

    @property
    def location(self):
        return self.__location

    @property
    def description(self):
        return self.__description

    @abstractmethod
    def report_type(self):
        """Return whether this is a lost or found report."""

    @abstractmethod
    def status_message(self):
        """Return a report-type-specific status message."""

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "reporter_name": self.reporter.name,
            "reporter_id": self.reporter.user_id,
            "date_reported": self.date_reported,
            "status": self.status,
            "type": self.report_type()
        }

    def display(self):
        print("-" * 55)
        print(f"Report ID   : {self.item_id}")
        print(f"Type        : {self.report_type()}")
        print(f"Item        : {self.name.title()}")
        print(f"Category    : {self.category.title()}")
        print(f"Location    : {self.location}")
        print(f"Description : {self.description}")
        print(f"Reported by : {self.reporter.get_details()}")
        print(f"Date        : {self.date_reported}")
        print(f"Status      : {self.status_message()}")
        print("-" * 55)


class LostItem(Item):
    def report_type(self):
        return "Lost"

    def status_message(self):
        if self.status == "Resolved":
            return "Item returned / case closed"
        return "Still searching"


class FoundItem(Item):
    def report_type(self):
        return "Found"

    def status_message(self):
        if self.status == "Resolved":
            return "Owner reunited with item / case closed"
        return "Waiting for its owner"


class CampusFind:
    """Manages reports, matching, searching and JSON persistence."""

    def __init__(self):
        self.items = []
        self.load_data()

    def generate_id(self):
        existing_numbers = []
        for item in self.items:
            try:
                existing_numbers.append(int(item.item_id[1:]))
            except (ValueError, IndexError):
                pass
        return f"R{max(existing_numbers, default=0) + 1:03d}"

    def add_report(self, report_type, name, category, location,
                   description, reporter):
        item_id = self.generate_id()
        item_class = LostItem if report_type == "Lost" else FoundItem
        item = item_class(item_id, name, category, location,
                          description, reporter)
        self.items.append(item)
        self.save_data()
        print(f"\nReport submitted successfully! Your report ID is {item_id}.")
        self.show_matches(item)

    def show_all(self, report_type=None, only_open=False):
        results = [
            item for item in self.items
            if (report_type is None or item.report_type() == report_type)
            and (not only_open or item.status == "Open")
        ]
        if not results:
            print("\nNo matching reports found.")
            return
        for item in results:
            item.display()

    def search(self, keyword):
        keyword = keyword.strip().lower()
        results = [
            item for item in self.items
            if item.status == "Open" and
            (keyword in item.name.lower()
             or keyword in item.category.lower()
             or keyword in item.location.lower()
             or keyword in item.description.lower())
        ]
        if not results:
            print("\nNo open reports matched your search.")
            return
        print(f"\nFound {len(results)} matching report(s):")
        for item in results:
            item.display()

    def show_matches(self, selected_item):
        """Suggest opposite-type reports with similar names or categories."""
        opposite = "Found" if selected_item.report_type() == "Lost" else "Lost"
        selected_words = set(selected_item.name.lower().split())
        matches = []

        for other in self.items:
            if other.item_id == selected_item.item_id:
                continue
            if other.status != "Open" or other.report_type() != opposite:
                continue

            same_category = other.category == selected_item.category
            other_words = set(other.name.lower().split())
            shared_words = selected_words.intersection(other_words)

            if same_category or shared_words:
                matches.append(other)

        if matches:
            print("\nPossible matches to check:")
            for match in matches:
                print(f"  {match.item_id} - {match.name.title()} "
                      f"({match.report_type()}, {match.location})")
            print("Please verify the item in person before claiming it.")
        else:
            print("\nNo possible matches yet. You can check again later.")

    def resolve_report(self, item_id):
        for item in self.items:
            if item.item_id.lower() == item_id.strip().lower():
                if item.status == "Resolved":
                    print("This report is already resolved.")
                else:
                    item.status = "Resolved"
                    self.save_data()
                    print(f"Report {item.item_id} marked as resolved.")
                return
        print("Report ID not found.")

    def save_data(self):
        data = [item.to_dict() for item in self.items]
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                records = json.load(file)
            for record in records:
                reporter = User(record["reporter_name"], record["reporter_id"])
                item_class = LostItem if record["type"] == "Lost" else FoundItem
                item = item_class(
                    record["item_id"], record["name"], record["category"],
                    record["location"], record["description"], reporter,
                    record.get("date_reported"), record.get("status", "Open")
                )
                self.items.append(item)
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Warning: saved data could not be loaded: {error}")


def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def create_report(portal, report_type):
    print(f"\n--- Report a {report_type} Item ---")
    name = get_nonempty("Item name: ")
    category = get_nonempty("Category (e.g., electronics, stationery): ")
    location = get_nonempty("Location (where lost/found): ")
    description = get_nonempty("Description / identifying details: ")
    reporter_name = get_nonempty("Your name: ")
    reporter_id = get_nonempty("Your student ID: ")
    portal.add_report(
        report_type, name, category, location, description,
        User(reporter_name, reporter_id)
    )


def main():
    portal = CampusFind()

    while True:
        print("\n" + "=" * 55)
        print("          CAMPUSFIND - LOST & FOUND PORTAL")
        print("=" * 55)
        print("1. Report a lost item")
        print("2. Report a found item")
        print("3. View all open reports")
        print("4. Search for an item")
        print("5. View only lost reports")
        print("6. View only found reports")
        print("7. Mark a report as resolved")
        print("8. Exit")
        print("=" * 55)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            create_report(portal, "Lost")
        elif choice == "2":
            create_report(portal, "Found")
        elif choice == "3":
            portal.show_all(only_open=True)
        elif choice == "4":
            keyword = get_nonempty("Enter item name, category or location: ")
            portal.search(keyword)
        elif choice == "5":
            portal.show_all(report_type="Lost", only_open=True)
        elif choice == "6":
            portal.show_all(report_type="Found", only_open=True)
        elif choice == "7":
            item_id = get_nonempty("Enter report ID (e.g., R001): ")
            portal.resolve_report(item_id)
        elif choice == "8":
            print("\nThank you for using CampusFind. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
