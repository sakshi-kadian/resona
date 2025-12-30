import httpClient from './https';
import { User } from '@/types/user';

/* Auth API */
export const authAPI = {
    /* Get current user information */
    getCurrentUser: async (): Promise<User> => {
        const response = await httpClient.get('/auth/me');
        return response.data;
    },
};

/* Profile API */
export const profileAPI = {
    /* Get complete user profile with all Spotify data */
    getCompleteProfile: async (): Promise<any> => {
        const response = await httpClient.get('/api/profile');
        return response.data;
    },

    /**
     * Get profile summary
     */
    getProfileSummary: async (): Promise<any> => {
        const response = await httpClient.get('/api/profile/summary');
        return response.data;
    },

    /* Compute ML features from user data */
    getFeatures: async (forceRefresh = false): Promise<any> => {
        const response = await httpClient.get(`/api/features?force_refresh=${forceRefresh}`);
        return response.data;
    },

    /* Get user's music taste cluster */
    getCluster: async (): Promise<any> => {
        const response = await httpClient.get('/api/cluster');
        return response.data;
    },

    /* Get personalized recommendations */
    getRecommendations: async (limit = 20): Promise<any> => {
        const response = await httpClient.get(`/api/recommendations?limit=${limit}`);
        return response.data;
    },

    /* Get listening statistics */
    getStatistics: async (): Promise<any> => {
        const response = await httpClient.get('/api/statistics');
        return response.data;
    },
};

/* Token Management */
export const tokenManager = {
    /* Save JWT token to localStorage */
    saveToken: (token: string): void => {
        localStorage.setItem('resona_token', token);
    },

    /* Get JWT token from localStorage */
    getToken: (): string | null => {
        return localStorage.getItem('resona_token');
    },

    /* Remove JWT token from localStorage */
    removeToken: (): void => {
        localStorage.removeItem('resona_token');
    },

    /* Check if user is authenticated */
    isAuthenticated: (): boolean => {
        return !!localStorage.getItem('resona_token');
    },
};

/* Auth helpers */
export const auth = {
    /* Redirect to Spotify login */
    login: (): void => {
        window.location.href = 'http://localhost:8000/auth/login';
    },

    /* Logout user */
    logout: (): void => {
        tokenManager.removeToken();
        window.location.href = '/';
    },
};
