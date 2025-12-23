import React, { useState, useEffect, useCallback } from 'react';
import { Comment, Task } from '../types';
import { commentApi, handleApiError } from '../services/api';
import CommentForm from './CommentForm';
import CommentItem from './CommentItem';

interface CommentListProps {
  task: Task;
  refreshTask?: () => void;
}

const CommentList: React.FC<CommentListProps> = ({ task, refreshTask }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingComment, setEditingComment] = useState<Comment | null>(null);

  const loadComments = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await commentApi.getCommentsByTask(task.id);
      setComments(response.comments);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  }, [task.id]);

  useEffect(() => {
    loadComments();
  }, [task.id, loadComments]);

  const handleCreateComment = async (commentData: { content: string; author_name: string; author_email?: string }) => {
    try {
      await commentApi.createComment({
        ...commentData,
        task_id: task.id,
      });
      await loadComments();
      if (refreshTask) refreshTask();
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const handleUpdateComment = async (id: number, commentData: { content?: string; author_name?: string; author_email?: string }) => {
    try {
      await commentApi.updateComment(id, commentData);
      await loadComments();
      setEditingComment(null);
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const handleDeleteComment = async (id: number) => {
    try {
      await commentApi.deleteComment(id);
      await loadComments();
      if (refreshTask) refreshTask();
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const startEditComment = (comment: Comment) => {
    setEditingComment(comment);
  };

  const cancelEditComment = () => {
    setEditingComment(null);
  };

  if (loading) {
    return (
      <div className="comments-loading">
        <div className="spinner">Loading comments...</div>
      </div>
    );
  }

  return (
    <div className="comment-list">
      <h3>Comments ({comments.length})</h3>
      
      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)} className="close-error">×</button>
        </div>
      )}

      <div className="add-comment-section">
        <CommentForm
          onSubmit={handleCreateComment}
          submitText="Add Comment"
          initialValues={{ content: '', author_name: '', author_email: '' }}
        />
      </div>

      {comments.length === 0 ? (
        <p className="no-comments">No comments yet. Be the first to comment!</p>
      ) : (
        <div className="comments-section">
          {comments.map((comment) => (
            <CommentItem
              key={comment.id}
              comment={comment}
              isEditing={editingComment?.id === comment.id}
              onUpdate={handleUpdateComment}
              onDelete={handleDeleteComment}
              onEdit={startEditComment}
              onCancelEdit={cancelEditComment}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default CommentList;
