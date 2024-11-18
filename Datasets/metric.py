import re
import pandas as pd

# Define a function to parse the full dataset
def parse_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    
    # Define regex patterns to extract necessary fields
    action_pattern = re.compile(r"Input Action: (.*)")
    output_pattern = re.compile(r"Output Action: (.*)")
    metric_pattern = re.compile(r"Metric: (.*)")
    
    # Initialize counters
    results = {
        "Order": {"TP": 0, "TN": 0, "FP": 0, "FN": 0},
        "Change": {"TP": 0, "TN": 0, "FP": 0, "FN": 0},
        "Remove": {"TP": 0, "TN": 0, "FP": 0, "FN": 0},
        "Option Add": {"TP": 0, "TN": 0, "FP": 0, "FN": 0},
    }

    # Split the dataset into individual entries
    entries = data.split("\n\n")
    
    # Loop through each entry to extract relevant information
    for entry in entries:
        input_action = re.search(action_pattern, entry)
        output_action = re.search(output_pattern, entry)
        metric = re.search(metric_pattern, entry)
        
        if input_action and output_action and metric:
            action_types = input_action.group(1).strip().split(", ")
            metric_value = metric.group(1).strip()

            # Update the counts based on the metric value for each action type
            for action_type in action_types:
                if action_type in results:
                    if metric_value == "TP":
                        results[action_type]["TP"] += 1
                    elif metric_value == "TN":
                        results[action_type]["TN"] += 1
                    elif metric_value == "FP":
                        results[action_type]["FP"] += 1
                    elif metric_value == "FN":
                        results[action_type]["FN"] += 1
                else:
                    print(f"Warning: Unrecognized action type '{action_type}' in entry:\n{entry}")

    return results


# Define a function to calculate metrics
def calculate_metrics(results):
    metrics = []

    for action, counts in results.items():
        TP = counts["TP"]
        TN = counts["TN"]
        FP = counts["FP"]
        FN = counts["FN"]
        total = TP + TN + FP + FN
        
        # Calculate precision, recall, accuracy, and F1 score
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        accuracy = (TP + TN) / total if total > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics.append([action, TP, TN, FP, FN, total, precision, recall, accuracy, f1_score])

    # Combine all results
    combined = {
        "TP": sum([counts["TP"] for counts in results.values()]),
        "TN": sum([counts["TN"] for counts in results.values()]),
        "FP": sum([counts["FP"] for counts in results.values()]),
        "FN": sum([counts["FN"] for counts in results.values()]),
    }
    combined_total = combined["TP"] + combined["TN"] + combined["FP"] + combined["FN"]
    combined_precision = combined["TP"] / (combined["TP"] + combined["FP"]) if (combined["TP"] + combined["FP"]) > 0 else 0
    combined_recall = combined["TP"] / (combined["TP"] + combined["FN"]) if (combined["TP"] + combined["FN"]) > 0 else 0
    combined_accuracy = (combined["TP"] + combined["TN"]) / combined_total if combined_total > 0 else 0
    combined_f1_score = (2 * combined_precision * combined_recall) / (combined_precision + combined_recall) if (combined_precision + combined_recall) > 0 else 0
    
    metrics.append(["Combined", combined["TP"], combined["TN"], combined["FP"], combined["FN"], combined_total,
                    combined_precision, combined_recall, combined_accuracy, combined_f1_score])
    
    return metrics

# Define a function to display the metrics table
def display_metrics_table(metrics):
    columns = ["Action Type", "TP", "TN", "FP", "FN", "Total", "Precision", "Recall", "Accuracy", "F1 Score"]
    df = pd.DataFrame(metrics, columns=columns)
    print(df)
    return df

# File path for the full dataset
file_path = "full_data.txt"

# Parse the dataset and calculate metrics
results = parse_dataset(file_path)
metrics = calculate_metrics(results)

# Display the metrics table
display_metrics_table(metrics)
