from flask import Blueprint, request, jsonify
from app.services.comment_service import CommentService
from app.services.task_service import TaskService

comment_bp = Blueprint('comments', __name__)

@comment_bp.route('/', methods=['GET'])
def get_comments():
    """Get all comments for a specific task."""
    try:
        task_id = request.args.get('task_id', type=int)
        if not task_id:
            return jsonify({'error': 'task_id parameter is required'}), 400
        
        # Verify task exists
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        comments = CommentService.get_comments_by_task(task_id)
        return jsonify({
            'comments': [comment.to_dict() for comment in comments],
            'count': len(comments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/', methods=['POST'])
def create_comment():
    """Create a new comment for a task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate data
        validated_data = CommentService.validate_comment_data(data)
        
        comment = CommentService.create_comment(validated_data)
        return jsonify(comment.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a specific comment by ID."""
    try:
        comment = CommentService.get_comment_by_id(comment_id)
        if not comment:
            return jsonify({'error': f'Comment with ID {comment_id} not found'}), 404
        
        return jsonify(comment.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update an existing comment."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate data
        validated_data = CommentService.validate_comment_data(data, is_update=True)
        
        comment = CommentService.update_comment(comment_id, validated_data)
        if not comment:
            return jsonify({'error': f'Comment with ID {comment_id} not found'}), 404
        
        return jsonify(comment.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment."""
    try:
        success = CommentService.delete_comment(comment_id)
        if not success:
            return jsonify({'error': f'Comment with ID {comment_id} not found'}), 404
        
        return jsonify({'message': f'Comment {comment_id} deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comment_bp.route('/task/<int:task_id>', methods=['GET'])
def get_task_comments(task_id):
    """Get all comments for a specific task (alternative endpoint)."""
    try:
        # Verify task exists
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': f'Task with ID {task_id} not found'}), 404
        
        comments = CommentService.get_comments_by_task(task_id)
        return jsonify({
            'task_id': task_id,
            'task_title': task.title,
            'comments': [comment.to_dict() for comment in comments],
            'count': len(comments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
