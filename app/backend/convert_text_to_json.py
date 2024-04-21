import re
import json

with open('IMG_1886.png.txt', 'r') as file:
    receipt_text = file.read()

# Regular expression to find items and prices
item_price_pattern = re.compile(r'(.*?)\s(\d+,\d+)$', re.MULTILINE)

# Extracting items and their prices
items = []
for match in item_price_pattern.finditer(receipt_text):
    item_name, price = match.groups()
    # Convert price format from "29,80" to a float "29.80"
    price = float(price.replace(',', '.'))
    items.append({
        "name": item_name.strip(),
        "price": price
    })

# Structuring the data as per the provided JSON example
receipt_data = {
    "store": {
        "name": "Eurospar Molde",
        "code": "Eurospar"
    },
    "items": items,
    "created_at": "07.11.23 10:35",
    "uploaded_at": "07.11.23 10:45"
}

# Convert to JSON
receipt_json = json.dumps(receipt_data, indent=4)

# Output the JSON for review before saving to a file
print(receipt_json)

# The JSON data would then be saved to a file named "receipt_example.json".
# This part will be implemented after reviewing the JSON output and ensuring it meets the requirements.


# Refining the extraction logic to better filter out non-item lines
refined_items = []

# Exclude specific lines by checking if they match known non-item patterns
exclude_patterns = [
    re.compile(r'^Sum\s\d+\svarer', re.IGNORECASE),
    re.compile(r'^BANK$', re.IGNORECASE),
    re.compile(r'^\d+,\d+\s+\d+,\d+\s+\d+,\d+$'),  # Matches the tax summary lines
    re.compile(r'^SUM\s+\d+,\d+\s+\d+,\d+$'),      # Matches the final sum line
    re.compile(r'^Totalbeløp:', re.IGNORECASE)
]

# Filtering out non-item entries
for item in items:
    if not any(pattern.match(item["name"]) for pattern in exclude_patterns):
        refined_items.append(item)

# Updating the dictionary with the refined items list
receipt_data["items"] = refined_items

# Convert to JSON again
receipt_json_refined = json.dumps(receipt_data, indent=4)

# Output the refined JSON for review before saving to a file
print(receipt_json_refined)

# After confirming the refined output meets the requirements, we will proceed to save it as a JSON file.

