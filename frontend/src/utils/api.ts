import axios from 'axios';
import { SearchResult } from '../types';

// API base URL - update this to match your backend server address
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request/response interceptors for debugging
api.interceptors.request.use(request => {
  console.log('API Request:', request);
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('API Response:', response);
    return response;
  },
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export interface SearchResponse {
  results: SearchResult[];
}

// API functions
export const apiService = {
  // Search documents with query
  async searchDocuments(query: string): Promise<SearchResult[]> {
    try {
      console.log('Searching for:', query);
      // Use direct string URL to avoid any encoding issues
      const response = await api.get(`/query?query=${encodeURIComponent(query)}`);
      
      console.log('Backend response type:', typeof response.data);
      console.log('Backend response:', response.data);
      
      // Handle different response formats
      let titles = [];
      
      if (Array.isArray(response.data)) {
        titles = response.data;
      } else if (response.data && typeof response.data === 'object') {
        // Try to extract data from possible API response structures
        if (Array.isArray(response.data.results)) {
          titles = response.data.results;
        } else if (Array.isArray(response.data.data)) {
          titles = response.data.data;
        } else if (typeof response.data === 'object') {
          // Last resort - try to find an array property
          const possibleArrays = Object.values(response.data).filter(val => Array.isArray(val));
          if (possibleArrays.length > 0) {
            titles = possibleArrays[0];
          }
        }
      }
      
      console.log('Extracted titles:', titles);
      
      // Map backend results to frontend SearchResult format
      return titles.map((title, index) => ({
        id: String(index + 1),
        title: typeof title === 'string' ? title : `Result ${index + 1}`,
        fileType: typeof title === 'string' ? (title.split('.').pop() || 'unknown') : 'unknown',
        excerpt: `Matched result for "${query}"...`,
        matchCount: Math.floor(Math.random() * 10) + 1,
        lastModified: new Date().toISOString().split('T')[0],
        size: '1.2 MB' // Placeholder
      }));
    } catch (error) {
      console.error('Error searching documents:', error);
      throw error; // Allow HomePage to handle the error
    }
  },

  // Upload a document
  async uploadDocument(file: File): Promise<{hashed_key: string; title: string}> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  },

  // Health check
  async checkAPIStatus(): Promise<boolean> {
    try {
      await api.get('/');
      return true;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  }
};