export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at: string;
  comments_count: number;
}

export interface Comment {
  id: number;
  content: string;
  author_name: string;
  author_email?: string;
  task_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateCommentRequest {
  content: string;
  author_name: string;
  author_email?: string;
  task_id: number;
}

export interface UpdateCommentRequest {
  content?: string;
  author_name?: string;
  author_email?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface TaskCommentsResponse {
  task: Task;
  comments: Comment[];
  comments_count: number;
}

export interface CommentsResponse {
  comments: Comment[];
  count: number;
}
