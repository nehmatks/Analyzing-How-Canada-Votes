import sys
import csv
from pathlib import Path
import matplotlib.pyplot as plt

def load_data(data_path, target_year):
    # Create an empty list to store our matching rows
    filtered_data = []

    try:
        with open(data_path, encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # Skip the header row
            
            for row in reader:
                # Make sure the row has exactly 4 columns to avoid errors
                if len(row) != 4:
                    continue
                
                # Convert the text into numbers
                row_year = int(row[0].strip())
                
                # Keep the row if the year matches (or if the user typed 0 for all years)
                if target_year == 0 or row_year == target_year:
                    province = row[1].strip()
                    turnout = float(row[2].strip())
                    wage_growth = float(row[3].strip())
                    
                    filtered_data.append((province, turnout, wage_growth))
                    
    except FileNotFoundError:
        # sys.exit() prints message and safely stops the program immediately
        sys.exit(f"Error: Could not find the file '{data_path}'")
    except ValueError:
        sys.exit("Error: The CSV file contains invalid numbers.")

    return filtered_data


def main():
    # Check if the user provided exactly 2 arguments in the terminal --> file and year
    if len(sys.argv) != 3:
        sys.exit("Usage: python make_graph.py <data_file.csv> <year> (Enter 0 for all years)")

    data_filename = sys.argv[1]
    
    # Turn the user's year input into an integer
    try:
        target_year = int(sys.argv[2])
    except ValueError:
        sys.exit("Error: The year must be a whole number.")
    
    # Load the data from the CSV
    data_path = Path(data_filename)
    results = load_data(data_path, target_year)
    
    if not results:
        sys.exit(f"Error: No data found for the year {target_year}.")

    # Sort the data by wage growth (as wage growth is the x axis)
    results.sort(key=lambda x: x[2])

    # Separate the data into distinct lists for plotting
    provinces = [item[0] for item in results]
    turnouts = [item[1] for item in results]
    wage_growths = [item[2] for item in results]

    print("Creating line graph...")

    # Set up and draw the graph
    plt.figure(figsize=(10, 6))
    plt.plot(wage_growths, turnouts, marker='o', linestyle='-', color='b')

    # Add province names next to each point
    for i, province in enumerate(provinces):
        plt.annotate(
            province, 
            (wage_growths[i], turnouts[i]), 
            textcoords="offset points", 
            xytext=(0, 10), 
            ha='center',
            fontsize=8
        )

    # Change the title depending on if they typed 0 or a specific year
    if target_year == 0:
        plt.title("Voter Turnout vs. Hourly Wage Growth in Canada (All Years)", fontsize=14)
    else:
        plt.title(f"Voter Turnout vs. Hourly Wage Growth in Canada ({target_year})", fontsize=14)

    plt.xlabel("Hourly Wage Growth (%)", fontsize=12)
    plt.ylabel("Voter Turnout (%)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Display the graph window
    plt.show()

if __name__ == "__main__":
    main()