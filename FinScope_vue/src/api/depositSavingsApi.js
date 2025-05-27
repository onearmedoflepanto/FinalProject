import axios from 'axios'; // Keep for FSS calls if they don't need auth
import api from './axios'; // Import the configured axios instance for authenticated calls

// const API_KEY = import.meta.env.VITE_FSS_API_KEY; // No longer needed for direct FSS call here
// const BASE_URL = '/api-fss/'; // No longer needed for direct FSS call here

export const fetchDepositProducts = async () => { // pageNo might not be needed if Django handles pagination or we fetch all
  try {
    // Calls the new Django backend endpoint
    // Using 'api' instance assuming it's configured for your Django backend URL
    const response = await api.get(`/api/accounts/financial-products/`, {
      params: {
        product_type: 'deposit'
        // Add other params like pageNo if your Django API supports pagination
      }
    });
    // The response.data will now be a list of FinancialProductSerializer output
    // console.log('Deposit products from Django API:', JSON.stringify(response.data, null, 2));
    return response.data; // This will be an array of products
  } catch (error) {
    console.error('Error fetching deposit products from Django API:', error);
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

// Function to toggle notification subscription for a saved financial product
export const toggleNotificationSubscription = async (savedProductId, notifyStatus) => {
  // savedProductId is the PK of the SavedFinancialProduct instance
  // notifyStatus is a boolean: true to subscribe, false to unsubscribe
  try {
    const response = await api.patch(`/api/accounts/saved-products/${savedProductId}/toggle-notification/`, {
      notify_on_rate_change: notifyStatus
    });
    return response.data; // Should return the updated SavedFinancialProduct object with the new status
  } catch (error) {
    console.error('Error toggling notification subscription:', error.response?.data || error.message);
    throw error.response?.data || error;
  }
};

export const fetchSavingsProducts = async () => { // pageNo might not be needed
  try {
    // Calls the new Django backend endpoint
    const response = await api.get(`/api/accounts/financial-products/`, {
      params: {
        product_type: 'savings'
        // Add other params like pageNo if your Django API supports pagination
      }
    });
    // The response.data will now be a list of FinancialProductSerializer output
    // console.log('Savings products from Django API:', JSON.stringify(response.data, null, 2));
    return response.data; // This will be an array of products
  } catch (error) {
    console.error('Error fetching savings products from Django API:', error);
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
