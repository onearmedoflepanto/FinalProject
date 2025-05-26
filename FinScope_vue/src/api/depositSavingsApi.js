import axios from 'axios'; // Keep for FSS calls if they don't need auth
import api from './axios'; // Import the configured axios instance for authenticated calls

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

// --- User Saved Financial Products ---

// Function to save a financial product for the logged-in user
export const saveFinancialProduct = async (productData) => {
  // productData should contain: { product_type, fin_co_no, fin_prdt_cd, product_name, bank_name }
  try {
    // Assumes your main authenticated axios instance is 'api' from '@/api/axios.js'
    // If this file uses a different axios instance, adjust accordingly or import the main one.
    // For simplicity, assuming 'axios' here refers to an instance that includes auth headers.
    // If not, you might need to import your configured axios instance: import api from './axios';
    const response = await api.post(`/api/accounts/saved-products/`, productData); 
    return response.data;
  } catch (error) {
    console.error('Error saving financial product:', error.response?.data || error.message);
    throw error.response?.data || error;
  }
};

// Function to unsave (delete) a financial product for the logged-in user
export const unsaveFinancialProduct = async (savedProductId) => {
  try {
    // Again, assuming 'axios' is configured with auth headers.
    await api.delete(`/api/accounts/saved-products/${savedProductId}/`);
    return { success: true, id: savedProductId }; // Return success and id for UI update
  } catch (error) {
    console.error('Error unsaving financial product:', error.response?.data || error.message);
    throw error.response?.data || error;
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
