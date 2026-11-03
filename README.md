# CampusFind – Smart Campus Lost & Found Portal

## Project overview
CampusFind is a menu-driven Python application that helps students report lost
and found belongings around a college campus. Users can submit reports, browse
open reports, search by keyword, see possible matches, and mark reports as
resolved.

## Features
- Report lost belongings.
- Report found belongings.
- Browse all open reports or filter by report type.
- Search by item name, category, location, or description.
- Suggest possible matches using shared categories or item-name words.
- Mark a report as resolved.
- Save reports in a JSON file so they remain available after the program closes.

## OOPS concepts demonstrated
1. **Class and object:** `User`, `Item`, `LostItem`, `FoundItem`, and `CampusFind`.
2. **Inheritance:** `LostItem` and `FoundItem` inherit common properties and
   behaviour from `Item`.
3. **Encapsulation:** `Item` stores its ID, name, category, location, and
   description in private attributes and exposes read-only properties.
4. **Abstraction:** `Item` is an abstract base class with abstract methods
   `report_type()` and `status_message()`.
5. **Polymorphism:** `LostItem` and `FoundItem` provide different implementations
   of the same abstract methods.

## Requirements
- Python 3.8 or newer
- No third-party packages required

## How to run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

4. Follow the numbered menu.

The program creates `campusfind_data.json` automatically when the first report
is submitted. Keep this file in the same folder as `main.py` to retain saved
reports.

## Example test flow
1. Choose `1` and report a lost item named `Blue Water Bottle`, category
   `accessories`, location `Cafeteria`.
2. Choose `2` and report a found item named `Blue Bottle`, category
   `accessories`, location `Library`.
3. The application should suggest the other report as a possible match because
   the categories are the same.
4. Choose `3` to view open reports.
5. Choose `7`, enter a report ID such as `R001`, and mark it resolved.
6. Exit and run the program again to verify that the JSON data is retained.

## Important note
The match feature provides suggestions only. A student should verify ownership
before returning an item. This is an academic demonstration, not an official
campus security or identity-verification system.

## Author
Add your name, registration number, course, and assessment details here before
submitting.
