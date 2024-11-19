// src/api/exchange.js
import axios from 'axios'

export const getExchangeRates = async () => {
  const { data } = await axios.get('http://localhost:8000/exchange/')
  return data
}