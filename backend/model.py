import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load simulated CSV data
df = pd.read_csv("energy_data.csv", names=["machine", "energy", "timestamp"])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day

# Encode machine names
df = pd.get_dummies(df, columns=['machine'], drop_first=True)

X = df.drop(["energy", "timestamp"], axis=1)
y = df["energy"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "energy_predictor.pkl")
print("Model trained and saved!")
