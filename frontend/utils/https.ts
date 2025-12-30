/**
 * HTTP Client Configuration
 * 
 * Axios instance with base configuration for API calls
 */

import axios from 'axios';

// Base API URL - change this for production
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
export const httpClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - add auth token to requests
httpClient.interceptors.request.use(
    (config) => {
        // Get token from localStorage
        const token = localStorage.getItem('resona_token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle errors
httpClient.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle 401 Unauthorized - token expired or invalid
        if (error.response?.status === 401) {
            // Clear token and redirect to login
            localStorage.removeItem('resona_token');
            window.location.href = '/';
        }

        return Promise.reject(error);
    }
);

export default httpClient;
