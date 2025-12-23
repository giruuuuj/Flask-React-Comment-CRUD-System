import axios from 'axios';
import { Task, Comment, CreateCommentRequest, UpdateCommentRequest, CommentsResponse, TaskCommentsResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Task API endpoints
export const taskApi = {
  getAllTasks: async (): Promise<Task[]> => {
    const response = await api.get('/tasks/');
    return response.data.tasks;
  },

  getTask: async (id: number): Promise<Task> => {
    const response = await api.get(`/tasks/${id}`);
    return response.data;
  },

  createTask: async (task: Partial<Task>): Promise<Task> => {
    const response = await api.post('/tasks/', task);
    return response.data;
  },

  updateTask: async (id: number, task: Partial<Task>): Promise<Task> => {
    const response = await api.put(`/tasks/${id}`, task);
    return response.data;
  },

  deleteTask: async (id: number): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },

  getTaskComments: async (taskId: number): Promise<TaskCommentsResponse> => {
    const response = await api.get(`/tasks/${taskId}/comments`);
    return response.data;
  },
};

// Comment API endpoints
export const commentApi = {
  getCommentsByTask: async (taskId: number): Promise<CommentsResponse> => {
    const response = await api.get(`/comments/?task_id=${taskId}`);
    return response.data;
  },

  getComment: async (id: number): Promise<Comment> => {
    const response = await api.get(`/comments/${id}`);
    return response.data;
  },

  createComment: async (comment: CreateCommentRequest): Promise<Comment> => {
    const response = await api.post('/comments/', comment);
    return response.data;
  },

  updateComment: async (id: number, comment: UpdateCommentRequest): Promise<Comment> => {
    const response = await api.put(`/comments/${id}`, comment);
    return response.data;
  },

  deleteComment: async (id: number): Promise<void> => {
    await api.delete(`/comments/${id}`);
  },

  getTaskComments: async (taskId: number): Promise<TaskCommentsResponse> => {
    const response = await api.get(`/comments/task/${taskId}`);
    return response.data;
  },
};

// Error handling utility
export const handleApiError = (error: any): string => {
  if (error.response) {
    return error.response.data.error || 'An error occurred';
  } else if (error.request) {
    return 'Network error. Please check your connection.';
  } else {
    return error.message || 'An unexpected error occurred';
  }
};

export default api;
