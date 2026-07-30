import { jwtDecode } from 'jwt-decode';

interface DecodedToken {
  user_id: string;
  email: string;
}

export const setToken = (token: string, userId: string) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('token', token);
  localStorage.setItem('userId', userId);
};

export const getToken = () => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
};

export const getUserId = () => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('userId');
};

export const removeToken = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('token');
  localStorage.removeItem('userId');
};