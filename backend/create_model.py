# Script to create a sample ML model for energy prediction
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Generate sample training data
np.random.seed(42)
n_samples = 1000

# Create sample data
data = {
    'machine': np.random.choice(['Machine_A', 'Machine_B', 'Machine_C'], n_samples),
    'hour': np.random.randint(0, 24, n_samples),
    'day': np.random.randint(1, 32, n_samples),
    'temperature': np.random.normal(25, 5, n_samples),
    'humidity': np.random.normal(60, 10, n_samples)
}

# Create energy consumption with some patterns
energy_base = {
    'Machine_A': 100,
    'Machine_B': 150, 
    'Machine_C': 200
}

energy_consumption = []
for i in range(n_samples):
    base = energy_base[data['machine'][i]]
    # Add hour effect (higher consumption during work hours)
    hour_effect = 50 if 8 <= data['hour'][i] <= 18 else 0
    # Add random noise
    noise = np.random.normal(0, 20)
    energy = base + hour_effect + noise
    energy_consumption.append(max(0, energy))  # Ensure non-negative

data['energy_consumption'] = energy_consumption

# Create DataFrame
df = pd.DataFrame(data)

# Prepare features
# One-hot encode machine
machine_dummies = pd.get_dummies(df['machine'], prefix='machine')
X = pd.concat([
    df[['hour', 'day', 'temperature', 'humidity']],
    machine_dummies
], axis=1)

y = df['energy_consumption']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'energy_predictor.pkl')

print("Model trained and saved as 'energy_predictor.pkl'")
print(f"Training R² score: {model.score(X_train, y_train):.3f}")
print(f"Test R² score: {model.score(X_test, y_test):.3f}")
print(f"Feature names: {list(X.columns)}")

# Also create a simplified model compatible with the current app.py format
# The app.py expects: hour, day, machine_Machine_B, machine_Machine_C
X_simple = pd.concat([
    df[['hour', 'day']],
    machine_dummies[['machine_Machine_B', 'machine_Machine_C']]  # Machine_A is reference
], axis=1)

X_train_simple, X_test_simple, y_train_simple, y_test_simple = train_test_split(
    X_simple, y, test_size=0.2, random_state=42
)

model_simple = RandomForestRegressor(n_estimators=100, random_state=42)
model_simple.fit(X_train_simple, y_train_simple)

# Override with the simplified model for deployment compatibility
joblib.dump(model_simple, 'energy_predictor.pkl')
print(f"\nDeployment-ready model saved!")
print(f"Simplified model features: {list(X_simple.columns)}")
print(f"Simplified model score: {model_simple.score(X_test_simple, y_test_simple):.3f}")
print("Model is ready for Render deployment!")