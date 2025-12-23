import React, { useState } from 'react';
import { Comment } from '../types';
import CommentForm from './CommentForm';

interface CommentItemProps {
  comment: Comment;
  isEditing: boolean;
  onUpdate: (id: number, data: { content?: string; author_name?: string; author_email?: string }) => void;
  onDelete: (id: number) => void;
  onEdit: (comment: Comment) => void;
  onCancelEdit: () => void;
}

const CommentItem: React.FC<CommentItemProps> = ({
  comment,
  isEditing,
  onUpdate,
  onDelete,
  onEdit,
  onCancelEdit,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleUpdate = async (data: { content?: string; author_name?: string; author_email?: string }) => {
    await onUpdate(comment.id, data);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this comment?')) {
      setIsDeleting(true);
      await onDelete(comment.id);
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (isEditing) {
    return (
      <div className="comment-item editing">
        <CommentForm
          onSubmit={handleUpdate}
          submitText="Update Comment"
          initialValues={{
            content: comment.content,
            author_name: comment.author_name,
            author_email: comment.author_email || '',
          }}
          onCancel={onCancelEdit}
        />
      </div>
    );
  }

  return (
    <div className="comment-item">
      <div className="comment-header">
        <div className="comment-author">
          <strong>{comment.author_name}</strong>
          {comment.author_email && (
            <span className="comment-email">({comment.author_email})</span>
          )}
        </div>
        <div className="comment-date">{formatDate(comment.created_at)}</div>
      </div>
      
      <div className="comment-content">
        {comment.content.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>

      <div className="comment-actions">
        <button
          onClick={() => onEdit(comment)}
          className="btn btn-sm btn-secondary"
          disabled={isDeleting}
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="btn btn-sm btn-danger"
          disabled={isDeleting}
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>

      {comment.updated_at !== comment.created_at && (
        <div className="comment-updated">
          <small>Updated: {formatDate(comment.updated_at)}</small>
        </div>
      )}
    </div>
  );
};

export default CommentItem;
