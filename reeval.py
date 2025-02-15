import json

# Load the JSON data
with open('dataset_latent_autointep_dataset_v2_info.json', 'r') as file:
    data = json.load(file)

# Initialize a list to store the results
results = []

# Iterate over each prompt in the dataset
for prompt_id, prompt_data in data.items():
    # Extract neuron data properly from "latents"
    unsafe_latents = prompt_data.get("unsafe_latent_info", {}).get("latents", {})
    safe_latents = prompt_data.get("safe_latent_data", {}).get("latents", {})

    # Get the neuron IDs from both unsafe and safe data
    unsafe_neurons = set(unsafe_latents.keys())  # Keys are the neuron IDs
    safe_neurons = set(safe_latents.keys())  # Keys are the neuron IDs

    # Find neurons that are **only in the unsafe section**
    exclusive_neurons = unsafe_neurons - safe_neurons

    if exclusive_neurons:
        # Extract auto_interp descriptions for exclusive neurons
        neuron_info = {
            neuron: unsafe_latents.get(neuron, {}).get("auto_interp", "No description")
            for neuron in exclusive_neurons
        }
        results.append(f'{prompt_id},"{neuron_info}"')

# Output the results
for result in results:
    print(result)


import csv

# Define the CSV file name
csv_filename = "harmful_only.csv"

# Write the results to the CSV file
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(["ID", "common_keys"])

    # Write each row
    for result in results:
        prompt_id, neuron_data = result.split(",", 1)  # Split prompt ID and neuron dictionary
        writer.writerow([prompt_id, neuron_data])

print(f"Data successfully saved to {csv_filename}!")
