// frontend/lib/api.ts
import { getToken } from './auth';

export const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export const toggleTaskCompletion = async (userId: string, taskId: string, completed: boolean): Promise<Task> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ completed }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to toggle task completion');
  }

  return response.json();
};

export const fetchTasks = async (userId: string): Promise<Task[]> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch tasks');
  }

  return response.json();
};

export const fetchTaskById = async (userId: string, taskId: string): Promise<Task> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch task by ID');
  }

  return response.json();
};


interface CreateTaskData {
    title: string;
    description?: string | null;
}

export const createTask = async (userId: string, taskData: CreateTaskData): Promise<Task> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create task');
  }

  return response.json();
};

interface UpdateTaskData {
    title?: string;
    description?: string | null;
    completed?: boolean;
}

export const updateTask = async (userId: string, taskId: string, taskData: UpdateTaskData): Promise<Task> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to update task');
  }

  return response.json();
};

export const deleteTask = async (userId: string, taskId: string): Promise<void> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to delete task');
  }
};

// Define types for chat messages
export interface ChatMessageRequest {
  message: string;
}

export interface ChatMessageResponse {
  response: string;
  action_taken?: string | null;
  action_details?: Record<string, any> | null;
}

export const sendChatMessage = async (chatRequest: ChatMessageRequest): Promise<ChatMessageResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found.');
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/chat/send-message`, { // Note the /v1/chat prefix
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(chatRequest),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to send chat message');
  }

  return response.json();
};

