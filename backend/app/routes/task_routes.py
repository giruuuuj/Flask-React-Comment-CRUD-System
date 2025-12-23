from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.services.comment_service import CommentService

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    try:
        tasks = TaskService.get_all_tasks()
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        task = TaskService.create_task(data)
        return jsonify(task.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID."""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        return jsonify(task.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        task = TaskService.update_task(task_id, data)
        if not task:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        return jsonify(task.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task and all its comments."""
    try:
        success = TaskService.delete_task(task_id)
        if not success:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        return jsonify({'message': f'Task {task_id} deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/<int:task_id>/comments', methods=['GET'])
def get_task_comments(task_id):
    """Get all comments for a specific task."""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        comments = CommentService.get_comments_by_task(task_id)
        return jsonify({
            'task': task.to_dict(),
            'comments': [comment.to_dict() for comment in comments],
            'comments_count': len(comments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
