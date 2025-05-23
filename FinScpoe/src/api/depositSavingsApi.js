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
    return response.data;
  } catch (error) {
    console.error('Error fetching deposit products:', error);
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
    return response.data;
  } catch (error) {
    console.error('Error fetching savings products:', error);
    throw error;
  }
};
