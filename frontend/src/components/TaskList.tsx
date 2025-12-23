import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { Task } from '../types';
import { taskApi, handleApiError } from '../services/api';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTaskForm, setShowTaskForm] = useState(false);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await taskApi.getAllTasks();
      setTasks(tasksData);
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData: Partial<Task>) => {
    try {
      setLoading(true);
      const newTask = await taskApi.createTask(taskData);
      setTasks(prev => [newTask, ...prev]);
      setShowTaskForm(false);
      toast.success('Task created successfully!');
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async (id: number, taskData: Partial<Task>) => {
    try {
      const updatedTask = await taskApi.updateTask(id, taskData);
      setTasks(prev => prev.map(task => 
        task.id === id ? updatedTask : task
      ));
      toast.success('Task updated successfully!');
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      toast.error(errorMessage);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await taskApi.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
      toast.success('Task deleted successfully!');
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
      toast.error(errorMessage);
    }
  };

  if (loading) {
    return (
      <div className="task-list-loading">
        Loading tasks...
      </div>
    );
  }

  return (
    <div className="task-list">
      <div className="task-list-header">
        <h2>Tasks ({tasks.length})</h2>
        <button
          onClick={() => setShowTaskForm(!showTaskForm)}
          className="btn btn-primary"
        >
          {showTaskForm ? 'Cancel' : 'Add New Task'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => setError(null)} className="close-error">×</button>
        </div>
      )}

      {showTaskForm && (
        <div className="task-form-section">
          <TaskForm
            onSubmit={handleCreateTask}
            submitText="Create Task"
            onCancel={() => setShowTaskForm(false)}
          />
        </div>
      )}

      {tasks.length === 0 ? (
        <p className="no-tasks">No tasks yet. Create your first task!</p>
      ) : (
        <div className="tasks-section">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={handleUpdateTask}
              onDelete={handleDeleteTask}
              onTaskUpdated={loadTasks}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;
