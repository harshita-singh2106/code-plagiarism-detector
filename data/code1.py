def is_safe_report(levels):
    # Check if the list is either increasing or decreasing
    is_increasing = all(levels[i] < levels[i+1] for i in range(len(levels) - 1))
    is_decreasing = all(levels[i] > levels[i+1] for i in range(len(levels) - 1))

    # If neither increasing nor decreasing, it's unsafe
    if not is_increasing and not is_decreasing:
        return False
    
    # Check if the difference between adjacent levels is between 1 and 3
    for i in range(len(levels) - 1):
        if abs(levels[i] - levels[i+1]) < 1 or abs(levels[i] - levels[i+1]) > 3:
            return False
    
    return True

def is_safe_with_one_removal(levels):
    # Try removing each level and check if the resulting list is safe
    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i+1:]
        if is_safe_report(new_levels):
            return True
    return False

def read_and_analyze_report(file_name):
    safe_reports_count = 0
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            levels = list(map(int, line.strip().split()))
            
            # First check if the report is safe, or if it's unsafe but can become safe with one removal
            if is_safe_report(levels) or is_safe_with_one_removal(levels):
                safe_reports_count += 1
    
    return safe_reports_count

# Main function to input file path
file_path = "E:\\Python projects\\input.txt" # Prompt user for file path
safe_reports = read_and_analyze_report(file_path)

print(f"Number of safe reports: {safe_reports}")
