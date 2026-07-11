import apiClient from './client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at?: string;
}

export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const res = await apiClient.post('/auth/login', data);
    return res.data;
  },

  register: async (data: RegisterRequest): Promise<UserResponse> => {
    const res = await apiClient.post('/auth/register', data);
    return res.data;
  },

  me: async (): Promise<UserResponse> => {
    const res = await apiClient.get('/auth/me');
    return res.data;
  },
};