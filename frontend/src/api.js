import axios from "axios";
const BASE_URL = "http://localhost:8000"; // or your deployed backend URL

export const predictEnergy = async (machine, hour, day) => {
  const response = await axios.post(`${BASE_URL}/predict`, { machine, hour, day });
  return response.data;
};
