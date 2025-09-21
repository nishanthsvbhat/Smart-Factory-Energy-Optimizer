import React, { useState } from "react";

export default function Dashboard() {
  const [machine, setMachine] = useState("Machine_A");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState("");

  const handlePredict = async () => {
    setLoading(true);
    try {
      const date = new Date();
      const hour = date.getHours();
      const day = date.getDate();

      // Use environment variable for API URL, with fallback
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      console.log('Attempting to connect to:', apiUrl);
      
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          machine: machine,
          hour: hour,
          day: day
        })
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      const energy = result.predicted_energy;
      setPrediction(energy);

      // Check for alerts and recommendations
      if (energy > 450) {
        setRecommendation(`High energy usage detected! Consider reducing load on ${machine}.`);
      } else {
        setRecommendation("");
      }
    } catch (error) {
      console.error("Prediction failed:", error);
      console.error("API URL was:", process.env.REACT_APP_API_URL || 'http://localhost:8000');
      
      if (error.message.includes('fetch')) {
        setRecommendation("⚠️ Backend not connected. Please deploy the backend first or check the API URL in environment variables.");
      } else {
        setRecommendation("Error: Unable to get prediction. Please check backend connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1 style={{ color: "#333", marginBottom: "30px" }}>Smart Factory Energy Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <label style={{ fontSize: "16px", fontWeight: "bold" }}>
          Select Machine: 
          <select 
            value={machine} 
            onChange={(e) => setMachine(e.target.value)}
            style={{ 
              marginLeft: "10px", 
              padding: "8px", 
              fontSize: "14px",
              borderRadius: "4px",
              border: "1px solid #ccc"
            }}
          >
            <option value="Machine_A">Machine A</option>
            <option value="Machine_B">Machine B</option>
            <option value="Machine_C">Machine C</option>
          </select>
        </label>
      </div>

      <div style={{ marginBottom: "30px" }}>
        <button 
          onClick={handlePredict}
          disabled={loading}
          style={{
            padding: "12px 24px",
            backgroundColor: loading ? "#ccc" : "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: "16px",
            fontWeight: "bold"
          }}
        >
          {loading ? "Predicting..." : "🔮 Predict Energy"}
        </button>
      </div>

      {prediction && (
        <div style={{ 
          marginBottom: "20px", 
          padding: "20px", 
          backgroundColor: "#e8f5e8", 
          border: "2px solid #4CAF50",
          borderRadius: "8px"
        }}>
          <h2 style={{ margin: "0 0 10px 0", color: "#2e7d32" }}>
            ⚡ Current Predicted Energy: {prediction} kWh
          </h2>
          <p style={{ margin: 0, color: "#555" }}>
            Machine: {machine} | Time: {new Date().toLocaleString()}
          </p>
        </div>
      )}

      {recommendation && (
        <div style={{ 
          marginBottom: "20px", 
          padding: "15px", 
          border: "2px solid orange", 
          backgroundColor: "#fff3e0",
          borderRadius: "8px"
        }}>
          <h3 style={{ margin: "0 0 10px 0", color: "#f57c00" }}>💡 Recommendation:</h3>
          <p style={{ margin: 0, color: "#555" }}>{recommendation}</p>
        </div>
      )}

      <div style={{ 
        marginTop: "30px", 
        padding: "15px", 
        backgroundColor: "#f5f5f5", 
        borderRadius: "8px",
        border: "1px solid #ddd"
      }}>
        <h3 style={{ margin: "0 0 10px 0", color: "#333" }}>📊 How it works:</h3>
        <ul style={{ margin: 0, color: "#666" }}>
          <li>Select a machine from the dropdown</li>
          <li>Click "Predict Energy" to get ML-powered predictions</li>
          <li>View real-time energy consumption forecasts</li>
          <li>Get optimization recommendations</li>
        </ul>
      </div>
    </div>
  );
}
