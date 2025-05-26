import axios from 'axios'

export async function fetchCommodityData(commodity) {
  const response = await axios.get('http://127.0.0.1:8000/api/stocks/commodities-summary/?mode=full')
  const rawData = response.data[commodity] || {}

  return Object.entries(rawData).map(([timestamp, price]) => ({
    Date: timestamp, // Keep the full timestamp string
    Price: price
  }))
}
