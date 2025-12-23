import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { Task } from '../types';
import TaskForm from './TaskForm';
import CommentList from './CommentList';

interface TaskItemProps {
  task: Task;
  onUpdate: (id: number, data: Partial<Task>) => void;
  onDelete: (id: number) => void;
  onTaskUpdated: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onUpdate,
  onDelete,
  onTaskUpdated,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showComments, setShowComments] = useState(false);

  const handleUpdate = async (data: Partial<Task>) => {
    await onUpdate(task.id, data);
    setIsEditing(false);
    toast.success('Task updated successfully!');
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task and all its comments?')) {
      await onDelete(task.id);
      toast.success('Task deleted successfully!');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'green';
      case 'in_progress': return 'blue';
      default: return 'gray';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      default: return 'green';
    }
  };

  if (isEditing) {
    return (
      <div className="task-item editing">
        <TaskForm
          onSubmit={handleUpdate}
          submitText="Update Task"
          initialValues={task}
          onCancel={() => setIsEditing(false)}
        />
      </div>
    );
  }

  return (
    <div className="task-item">
      <div className="task-header">
        <h3 className="task-title">{task.title}</h3>
        <div className="task-actions">
          <button
            onClick={() => setIsEditing(true)}
            className="btn btn-sm btn-secondary"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="btn btn-sm btn-danger"
          >
            Delete
          </button>
        </div>
      </div>

      {task.description && (
        <div className="task-description">
          <p>{task.description}</p>
        </div>
      )}

      <div className="task-meta">
        <span className={`task-status status-${getStatusColor(task.status)}`}>
          {task.status.replace('_', ' ')}
        </span>
        <span className={`task-priority priority-${getPriorityColor(task.priority)}`}>
          {task.priority}
        </span>
        <span className="task-comments-count">
          {task.comments_count} {task.comments_count === 1 ? 'comment' : 'comments'}
        </span>
      </div>

      <div className="task-footer">
        <button
          onClick={() => setShowComments(!showComments)}
          className="btn btn-sm btn-outline"
        >
          {showComments ? 'Hide Comments' : 'Show Comments'}
        </button>
        <small className="task-date">
          Created: {new Date(task.created_at).toLocaleDateString()}
        </small>
      </div>

      {showComments && (
        <div className="task-comments">
          <CommentList task={task} refreshTask={onTaskUpdated} />
        </div>
      )}
    </div>
  );
};

export default TaskItem;
