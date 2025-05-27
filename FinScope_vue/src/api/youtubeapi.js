import axios from 'axios'

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const BASE_URL = "https://www.googleapis.com/youtube/v3"
const youtubeApi = axios.create({
  baseURL: BASE_URL
})

export const getVideoDetails = async (videoId) => {
  try {
    const response = await youtubeApi.get("/videos", {
      params: {
        part: "snippet,statistics",
        id: videoId,
        key: API_KEY
      }
    })
    return response.data.items[0]
  } catch (error) {
    console.error("API Error:", error)
    throw error
  }
}

export const searchVideos = async (query, baseURL = BASE_URL, factor = "주식") => {
  try {
    const youtubeApi = axios.create({
      baseURL: baseURL
    })

    const response = await youtubeApi.get("/search", {
      params: {
        part: "snippet",
        maxResults: 10,
        q: query + " " + factor,
        type: "video",
        relevanceLanguage: "ko",
        key: API_KEY
      }
    })

    const decodedItems = response.data.items.map((item) => {
      return {
        ...item,
        snippet: {
          ...item.snippet,
          title: decodeHtmlEntities(item.snippet.title),
          description: decodeHtmlEntities(item.snippet.description)
        }
      }
    })

    return decodedItems
  } catch (error) {
    console.error("API Error:", error)
    throw error
  }
}

function decodeHtmlEntities(text) {
  const textArea = document.createElement("textarea")
  textArea.innerHTML = text
  return textArea.value
}
