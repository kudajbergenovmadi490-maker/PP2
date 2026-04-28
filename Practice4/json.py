# ============================================================
# Python JSON Module
# JSON = JavaScript Object Notation — universal data format
# ============================================================

import sys
import os

# NOTE: This file is named json.py which shadows the stdlib json module.
# We temporarily remove the current directory from sys.path so Python
# finds the real stdlib json instead of this file.
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir in sys.path:
    sys.path.remove(_this_dir)
import json
sys.path.insert(0, _this_dir)  # restore it after import

print("=== JSON BASICS ===")

# --- JSON Syntax overview ---
# JSON uses:
#   {} for objects (like Python dicts)
#   [] for arrays  (like Python lists)
#   strings must use double quotes
#   true/false (lowercase) instead of True/False
#   null instead of None


# --- Parsing JSON: json.loads() ---
# Converts a JSON STRING into a Python object
print("\n--- json.loads() — string to Python ---")

json_string = '{"name": "Alice", "age": 30, "active": true, "score": null}'
python_obj = json.loads(json_string)

print(f"JSON string: {json_string}")
print(f"Python dict: {python_obj}")
print(f"Type:        {type(python_obj)}")
print(f"Name:        {python_obj['name']}")
print(f"Age:         {python_obj['age']}")
print(f"Active:      {python_obj['active']}")  # true -> True
print(f"Score:       {python_obj['score']}")   # null -> None

# Parsing a JSON array
json_array = '[1, 2, 3, "hello", true, null]'
python_list = json.loads(json_array)
print(f"\nJSON array:  {json_array}")
print(f"Python list: {python_list}")
print(f"Type:        {type(python_list)}")

# Nested JSON
json_nested = '''
{
    "user": {
        "id": 42,
        "name": "Bob",
        "address": {
            "city": "Almaty",
            "country": "Kazakhstan"
        },
        "hobbies": ["coding", "chess", "hiking"]
    }
}
'''
data = json.loads(json_nested)
print(f"\nNested JSON parsing:")
print(f"  User:    {data['user']['name']}")
print(f"  City:    {data['user']['address']['city']}")
print(f"  Hobbies: {data['user']['hobbies']}")


# --- Converting Python to JSON: json.dumps() ---
# Converts a Python object into a JSON STRING
print("\n=== json.dumps() — Python to string ===")

person = {
    "name": "Charlie",
    "age": 25,
    "active": True,        # -> true
    "score": None,         # -> null
    "tags": ["python", "dev"]
}

# Basic conversion
json_str = json.dumps(person)
print(f"Compact JSON: {json_str}")

# Pretty-printed with indent
json_pretty = json.dumps(person, indent=4)
print(f"\nPretty JSON:\n{json_pretty}")

# Sort keys alphabetically
json_sorted = json.dumps(person, indent=2, sort_keys=True)
print(f"\nSorted keys:\n{json_sorted}")

# JSON type mapping reference
print("\n--- Python <-> JSON type mapping ---")
mapping = {
    "Python dict":   "JSON object {}",
    "Python list":   "JSON array []",
    "Python str":    "JSON string",
    "Python int":    "JSON number",
    "Python float":  "JSON number",
    "Python True":   "JSON true",
    "Python False":  "JSON false",
    "Python None":   "JSON null",
}
for py_type, json_type in mapping.items():
    print(f"  {py_type:<20} -> {json_type}")


# --- Writing JSON to a file ---
print("\n=== WRITING JSON FILES ===")

script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, "output_employees.json")

employees = [
    {"id": 1, "name": "Alice",   "department": "Engineering", "salary": 85000},
    {"id": 2, "name": "Bob",     "department": "Marketing",   "salary": 65000},
    {"id": 3, "name": "Charlie", "department": "Engineering", "salary": 95000},
]

with open(output_file, "w") as f:
    json.dump(employees, f, indent=4)

print(f"Written {len(employees)} employees to 'output_employees.json'")


# --- Reading JSON from a file ---
print("\n=== READING JSON FILES ===")

sample_file = os.path.join(script_dir, "sample-data.json")
if os.path.exists(sample_file):
    with open(sample_file, "r") as f:
        company = json.load(f)

    print(f"Company: {company['company']}")
    print(f"Founded: {company['founded']}")
    print(f"Office:  {company['office']['city']}, {company['office']['country']}")

    print(f"\nEmployees ({len(company['employees'])}):")
    for emp in company['employees']:
        print(f"  [{emp['id']}] {emp['name']} -- {emp['department']} -- ${emp['salary']:,}")

    # Filter: Engineering employees
    engineers = [e for e in company['employees'] if e['department'] == 'Engineering']
    print(f"\nEngineers: {[e['name'] for e in engineers]}")

    # Average salary
    avg_salary = sum(e['salary'] for e in company['employees']) / len(company['employees'])
    print(f"Average salary: ${avg_salary:,.0f}")

    # Find employee with most skills
    most_skills = max(company['employees'], key=lambda e: len(e['skills']))
    print(f"Most skills: {most_skills['name']} ({len(most_skills['skills'])} skills)")
else:
    print(f"'sample-data.json' not found -- skipping.")

# Read back the file we wrote
print(f"\nReading back 'output_employees.json':")
with open(output_file, "r") as f:
    loaded = json.load(f)
for emp in loaded:
    print(f"  {emp['name']} -- {emp['department']}")


# --- Working with JSON data ---
print("\n=== WORKING WITH JSON DATA ===")

with open(output_file, "r") as f:
    data = json.load(f)

# Add a new employee
data.append({"id": 4, "name": "Diana", "department": "Design", "salary": 72000})

# Give everyone a 10% raise
for emp in data:
    emp['salary'] = int(emp['salary'] * 1.1)

with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print("After 10% raise and adding Diana:")
with open(output_file, "r") as f:
    updated = json.load(f)
for emp in updated:
    print(f"  {emp['name']}: ${emp['salary']:,}")

# Round-trip test
print("\n--- Round-trip test ---")
original = {"key": "value", "numbers": [1, 2, 3], "flag": True}
serialized = json.dumps(original)
deserialized = json.loads(serialized)
print(f"Original == Deserialized: {original == deserialized}")  # True

# Clean up
os.remove(output_file)
