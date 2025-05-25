import axios from 'axios';

const API_KEY = import.meta.env.VITE_FSS_API_KEY;
const BASE_URL = '/api-fss/'; // Use the proxied path

export const fetchDepositProducts = async (pageNo = 1) => {
  try {
    const response = await axios.get(`${BASE_URL}depositProductsSearch.json`, {
      params: {
        auth: API_KEY,
        topFinGrpNo: '020000', // 은행 (Bank)
        pageNo: pageNo
      }
    });
    console.log('Deposit products API response:', JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    console.error('Error fetching deposit products:', error);
    if (error.response) {
      console.error('Error response data:', JSON.stringify(error.response.data, null, 2));
      console.error('Error response status:', error.response.status);
      console.error('Error response headers:', error.response.headers);
    } else if (error.request) {
      console.error('Error request:', error.request);
    } else {
      console.error('Error message:', error.message);
    }
    throw error;
  }
};

export const fetchSavingsProducts = async (pageNo = 1) => {
  try {
    const response = await axios.get(`${BASE_URL}savingProductsSearch.json`, {
      params: {
        auth: API_KEY,
        topFinGrpNo: '020000', // 은행 (Bank)
        pageNo: pageNo
      }
    });
    console.log('Savings products API response:', JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    console.error('Error fetching savings products:', error);
    if (error.response) {
      console.error('Error response data:', JSON.stringify(error.response.data, null, 2));
      console.error('Error response status:', error.response.status);
      console.error('Error response headers:', error.response.headers);
    } else if (error.request) {
      console.error('Error request:', error.request);
    } else {
      console.error('Error message:', error.message);
    }
    throw error;
  }
};
