import re

# Define the input file path
file_path = "full_data.txt"

# Define dictionaries to store data based on input actions
data = {
    "Order": [],
    "Change": [],
    "Option Add": [],
    "Remove": []
}

# Regular expression to match the input action
input_action_regex = r"Input Action: (Order|Change|Option Add|Remove)"

# Read and parse the dataset
with open(file_path, 'r', encoding='utf-8') as file:
    entry = []
    current_action = None

    for line in file:
        # Check for a new input action
        action_match = re.search(input_action_regex, line)
        if action_match:
            # If there's an existing entry, add it to the corresponding list
            if current_action and entry:
                data[current_action].append("\n".join(entry))
                entry = []

            # Update the current action
            current_action = action_match.group(1)

        # Add the line to the current entry
        entry.append(line.strip())

    # Add the last entry to the list
    if current_action and entry:
        data[current_action].append("\n".join(entry))

# Write the separated datasets into different files
for action_type, entries in data.items():
    output_file = f"{action_type.lower().replace(' ', '_')}_dataset.txt"
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("\n\n".join(entries))
    print(f"Dataset for '{action_type}' saved to: {output_file}")
