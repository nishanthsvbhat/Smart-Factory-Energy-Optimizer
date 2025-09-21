import random
import time
import pandas as pd
from datetime import datetime
import os

MACHINES = ["Machine_A", "Machine_B", "Machine_C"]

# Base energy consumption for each machine (kWh)
MACHINE_BASE_CONSUMPTION = {
    "Machine_A": {"min": 50, "max": 200},
    "Machine_B": {"min": 100, "max": 300}, 
    "Machine_C": {"min": 150, "max": 450}
}

def generate_energy_data():
    """Generate realistic energy consumption data for all machines"""
    data = []
    current_hour = datetime.now().hour
    
    for machine in MACHINES:
        base_config = MACHINE_BASE_CONSUMPTION[machine]
        
        # Add time-based variation (higher consumption during work hours)
        if 8 <= current_hour <= 18:  # Work hours
            multiplier = random.uniform(1.2, 1.5)
        elif 6 <= current_hour <= 7 or 19 <= current_hour <= 21:  # Transition hours
            multiplier = random.uniform(0.8, 1.2)
        else:  # Night hours
            multiplier = random.uniform(0.3, 0.8)
        
        # Calculate energy with some randomness
        base_energy = random.uniform(base_config["min"], base_config["max"])
        energy = round(base_energy * multiplier, 2)
        
        timestamp = datetime.now()
        data.append({
            "machine": machine, 
            "energy": energy, 
            "timestamp": timestamp,
            "hour": current_hour
        })
    return data

def save_to_csv(data, filename="energy_data.csv"):
    """Save data to CSV file"""
    df = pd.DataFrame(data)
    
    # Create header if file doesn't exist
    file_exists = os.path.exists(filename)
    mode = 'a' if file_exists else 'w'
    header = False if file_exists else True
    
    df.to_csv(filename, mode=mode, header=header, index=False)

def print_summary_stats(filename="energy_data.csv"):
    """Print summary statistics of generated data"""
    try:
        df = pd.read_csv(filename)
        print("\n" + "="*60)
        print("ENERGY CONSUMPTION SUMMARY")
        print("="*60)
        
        for machine in MACHINES:
            machine_data = df[df['machine'] == machine]
            if len(machine_data) > 0:
                avg_energy = machine_data['energy'].mean()
                min_energy = machine_data['energy'].min()
                max_energy = machine_data['energy'].max()
                print(f"{machine:12} | Avg: {avg_energy:6.1f} kWh | Min: {min_energy:6.1f} | Max: {max_energy:6.1f}")
        
        print(f"\nTotal records: {len(df)}")
        print(f"Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
    except Exception as e:
        print(f"Error reading summary: {e}")

if __name__ == "__main__":
    print("IoT Energy Data Simulator Starting...")
    print("Press Ctrl+C to stop the simulation")
    print("-" * 50)
    
    try:
        iteration = 0
        while True:
            iteration += 1
            data = generate_energy_data()
            save_to_csv(data)
            
            print(f"\nIteration {iteration} - {datetime.now().strftime('%H:%M:%S')}")
            for entry in data:
                print(f"  {entry['machine']}: {entry['energy']:6.1f} kWh")
            
            # Print summary every 10 iterations
            if iteration % 10 == 0:
                print_summary_stats()
            
            time.sleep(5)  # Generate every 5 seconds
            
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user.")
        print_summary_stats()
        print("Data saved to energy_data.csv")
