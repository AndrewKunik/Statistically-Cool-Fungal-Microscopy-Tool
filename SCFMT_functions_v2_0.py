import numpy as np

# Function to calculate basic statistics
def calculate_statistics(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    return mean, std_dev

# Function to identify outliers using the Interquartile Range (IQR) method
def identify_outliers_iqr(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_low = [x for x in data if x < lower_bound]
    outliers_high = [x for x in data if x > upper_bound]
    return lower_bound, upper_bound, outliers_low, outliers_high

# Function to analyze and format the output for a single dimension
def analyze_dimension(data, label):
    """Analyze a set of measurements and format the output for a given label."""
    mean, std_dev = calculate_statistics(data)
    lower_bound, upper_bound, outliers_low, outliers_high = identify_outliers_iqr(data)
    central_range_min = np.min([x for x in data if x >= lower_bound])
    central_range_max = np.max([x for x in data if x <= upper_bound])
    outliers_str_low = f"({min(outliers_low)})" if outliers_low else ""
    outliers_str_high = f"({max(outliers_high)})" if outliers_high else ""
    return f"{label} = {outliers_str_low}{central_range_min}–{central_range_max}{outliers_str_high} µm, average = {mean:.1f} ± {std_dev:.1f} µm"

# Main function to analyze all measurements for a given structure
def analyze_structure(structure_name, measurements, calculate_q=False):
    """
    Analyze various dimensions for a given fungal structure.
    """
    results = []
    q_values = None
    n_info = []

    # Analyze each dimension separately
    for label, values in measurements.items():
        if not values.strip():  # Skip empty strings
            continue

        values_list = list(map(float, values.split(',')))
        result = analyze_dimension(values_list, label)
        results.append(result)
        n_info.append(f"{label} (n = {len(values_list)})")
        
        # If we need to calculate Q ratio, track length and width
        if calculate_q and label in ['length', 'width']:
            if q_values is None:
                q_values = {}
            q_values[label] = values_list

    # Calculate Q ratio if length and width are present
    if calculate_q and q_values and 'length' in q_values and 'width' in q_values:
        Q_values = [l / w for l, w in zip(q_values['length'], q_values['width'])]
        Q_mean, Q_std_dev = calculate_statistics(Q_values)
        Q_output = f"Q = {min(Q_values):.2f}–{max(Q_values):.2f} (average = {Q_mean:.2f} ± {Q_std_dev:.2f})"
        results.append(Q_output)

    # Include sample sizes in a separate section, not within the text
    n_output = "; ".join(n_info)
    return f"{structure_name.capitalize()} Analysis (Sample Sizes: {n_output}):\n" + "; ".join(results) + "\n"

# Function to analyze multiple structures at once
def analyze_all_structures(structures):
    """
    Analyze multiple fungal structures at once.
    """
    analysis_results = []
    for structure_name, (measurements, calculate_q) in structures.items():
        analysis_results.append(analyze_structure(structure_name, measurements, calculate_q))
    return "\n".join(analysis_results)