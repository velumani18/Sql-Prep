import { apiRequest } from './apiClient';

export interface User {
  id: string;
  name: string;
  email: string;
  avatar_url: string;
  streak_days: number;
  xp: number;
  level_title: string;
  last_active?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export const authService = {
  async login(email: string, password: string = 'password'): Promise<AuthResponse> {
    const res = await apiRequest<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('sqlforge_token', res.token);
    localStorage.setItem('sqlforge_user', JSON.stringify(res.user));
    return res;
  },

  async signup(name: string, email: string, password: string = 'password'): Promise<AuthResponse> {
    const res = await apiRequest<AuthResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
    localStorage.setItem('sqlforge_token', res.token);
    localStorage.setItem('sqlforge_user', JSON.stringify(res.user));
    return res;
  },

  async logout(): Promise<void> {
    try {
      await apiRequest('/auth/logout', { method: 'POST' });
    } catch {
      // Ignore network errors on logout
    }
    localStorage.removeItem('sqlforge_token');
    localStorage.removeItem('sqlforge_user');
  },

  async getCurrentUser(): Promise<User> {
    try {
      const user = await apiRequest<User>('/auth/me');
      localStorage.setItem('sqlforge_user', JSON.stringify(user));
      return user;
    } catch {
      const cached = localStorage.getItem('sqlforge_user');
      if (cached) {
        return JSON.parse(cached);
      }
      return {
        id: 'usr-demo',
        name: 'Alex Developer',
        email: 'alex.dev@sqlforge.dev',
        avatar_url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces',
        streak_days: 5,
        xp: 850,
        level_title: 'SQL Practitioner',
      };
    }
  },
};

