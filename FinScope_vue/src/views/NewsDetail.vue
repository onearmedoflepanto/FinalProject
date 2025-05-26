<template>
  <div class="news-detail-container p-4">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">{{ newsItem.title }}</h1>
    <img v-if="newsItem.imageUrl" :src="newsItem.imageUrl" alt="뉴스 이미지" class="mb-6 max-w-full h-auto rounded-lg shadow-md">
    <div class="meta-info text-sm text-gray-600 mb-4">
      <p class="mb-1"><strong>출처:</strong> {{ newsItem.source }}</p>
      <p><strong>게시일:</strong> {{ formatDate(newsItem.publishedAt) }}</p>
    </div>
    <div class="news-content prose prose-lg mt-6 text-gray-700">
      <p style="white-space: pre-line;">{{ newsItem.content }}</p>
    </div>
    <router-link to="/" class="text-indigo-600 hover:text-indigo-800 hover:underline mt-8 inline-block font-medium">뉴스 목록으로 돌아가기</router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/axios'; // Import the api instance

const route = useRoute();
const newsItem = ref({
  title: 'Loading news...',
  source: '',
  publishedAt: '',
  content: 'Please wait while we fetch the news content.',
  imageUrl: '',
  originalLink: ''
});

// Function to fetch news details from the backend
const fetchNewsDetail = async (newsUrl) => {
  console.log(`Attempting to fetch news details for URL: ${newsUrl}`);
  newsItem.value = { // Reset to loading state
    title: 'Fetching news details...',
    source: '',
    publishedAt: '',
    content: 'Loading content from server...',
    imageUrl: '',
    originalLink: newsUrl
  };

  if (typeof newsUrl !== 'string' || !newsUrl.trim()) {
    console.error('fetchNewsDetail called with invalid newsUrl:', newsUrl);
    newsItem.value = {
      title: 'Error: Invalid News URL',
      source: '',
      publishedAt: '',
      content: 'Cannot process an empty or invalid news URL. Please ensure a valid URL is provided.',
      imageUrl: '',
      originalLink: String(newsUrl || '')
    };
    return;
  }

  try {
    // Make API call to backend to scrape/fetch news
    // Assuming backend endpoint /api/news/scrape/?url=<encoded_url>
    const response = await api.get('/api/news/scrape/', {
      params: { url: newsUrl }
    });

    if (response.data) {
      newsItem.value = {
        title: response.data.title || 'Title not available',
        source: response.data.source || 'Source not available',
        publishedAt: response.data.publishedAt || '',
        content: response.data.content || 'Content not available.',
        imageUrl: response.data.imageUrl || '', // Use placeholder if not provided by API?
        originalLink: response.data.originalLink || newsUrl
      };
      console.log('News item populated from API:', newsItem.value);
    } else {
      throw new Error('API response did not contain data.');
    }
  } catch (error) {
    console.error(`Error fetching news detail for URL '${newsUrl}':`, error);
    let errorMessage = `Failed to load news content.`;
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      errorMessage += ` Server responded with ${error.response.status}: ${error.response.data.detail || error.response.statusText}`;
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage += ` No response received from server. Please check your network connection and the backend server.`;
    } else {
      // Something happened in setting up the request that triggered an Error
      errorMessage += ` Error: ${error.message}`;
    }
    newsItem.value = {
      title: 'Error: Could not load news',
      source: '',
      publishedAt: '',
      content: errorMessage,
      imageUrl: '',
      originalLink: newsUrl
    };
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  } catch (e) {
    console.error("Error formatting date:", dateString, e);
    return 'Invalid Date';
  }
};

onMounted(() => {
  const newsUrlFromQuery = route.query.url;
  console.log('NewsDetail.vue mounted. URL from query:', newsUrlFromQuery);

  if (newsUrlFromQuery && typeof newsUrlFromQuery === 'string' && newsUrlFromQuery.trim()) {
    fetchNewsDetail(newsUrlFromQuery);
  } else {
    console.error('News URL not found in query parameters or is invalid:', newsUrlFromQuery);
    newsItem.value = {
      title: 'Error: News URL not provided or invalid',
      source: '',
      publishedAt: '',
      content: 'Cannot load news details because the URL was not found in the page address or it was invalid.',
      imageUrl: '',
      originalLink: String(newsUrlFromQuery || '')
    };
  }
});
</script>

<style scoped>
.news-detail-container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.news-content {
  line-height: 1.75; /* Increased line height for better readability */
  font-size: 1.1rem; /* Slightly larger font for content */
}

.news-content p {
  margin-bottom: 1.25em; /* Add some space between paragraphs if rendered separately */
}

.meta-info {
  border-bottom: 1px solid #e5e7eb; /* Light gray border */
  padding-bottom: 1rem;
}

/* Additional styling for prose can be added if Tailwind Prose plugin is not fully covering needs */
.prose h1, .prose h2, .prose h3 {
  color: #374151; /* Darker headings within prose if needed */
}
</style>
