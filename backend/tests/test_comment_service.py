import pytest
from app.services.comment_service import CommentService
from app.services.task_service import TaskService
from app.models import Comment, Task

class TestCommentService:
    """Test cases for comment service layer."""
    
    def test_get_comments_by_task(self, app, sample_task, sample_comment):
        """Test getting comments by task ID."""
        with app.app_context():
            comments = CommentService.get_comments_by_task(sample_task.id)
            assert len(comments) == 1
            assert comments[0].id == sample_comment.id
            assert comments[0].content == sample_comment.content
    
    def test_get_comments_empty_task(self, app, sample_task):
        """Test getting comments for task with no comments."""
        with app.app_context():
            comments = CommentService.get_comments_by_task(sample_task.id)
            assert len(comments) == 0
    
    def test_get_comment_by_id(self, app, sample_comment):
        """Test getting comment by ID."""
        with app.app_context():
            comment = CommentService.get_comment_by_id(sample_comment.id)
            assert comment is not None
            assert comment.id == sample_comment.id
            assert comment.content == sample_comment.content
    
    def test_get_nonexistent_comment(self, app):
        """Test getting non-existent comment."""
        with app.app_context():
            comment = CommentService.get_comment_by_id(999)
            assert comment is None
    
    def test_create_comment_success(self, app, sample_task):
        """Test successful comment creation."""
        comment_data = {
            'content': 'New test comment',
            'author_name': 'Test User',
            'author_email': 'test@example.com',
            'task_id': sample_task.id
        }
        
        with app.app_context():
            comment = CommentService.create_comment(comment_data)
            assert comment.content == comment_data['content']
            assert comment.author_name == comment_data['author_name']
            assert comment.task_id == sample_task.id
            assert comment.id is not None
            assert comment.created_at is not None
    
    def test_create_comment_nonexistent_task(self, app):
        """Test creating comment for non-existent task."""
        comment_data = {
            'content': 'Test comment',
            'author_name': 'Test User',
            'task_id': 999
        }
        
        with app.app_context():
            with pytest.raises(ValueError, match="Task with ID 999 not found"):
                CommentService.create_comment(comment_data)
    
    def test_create_comment_missing_content(self, app, sample_task):
        """Test creating comment with missing content."""
        comment_data = {
            'author_name': 'Test User',
            'task_id': sample_task.id
        }
        
        with app.app_context():
            with pytest.raises(ValueError, match="Content and author_name are required"):
                CommentService.create_comment(comment_data)
    
    def test_create_comment_missing_author(self, app, sample_task):
        """Test creating comment with missing author name."""
        comment_data = {
            'content': 'Test comment',
            'task_id': sample_task.id
        }
        
        with app.app_context():
            with pytest.raises(ValueError, match="Content and author_name are required"):
                CommentService.create_comment(comment_data)
    
    def test_update_comment_success(self, app, sample_comment):
        """Test successful comment update."""
        update_data = {
            'content': 'Updated content',
            'author_name': 'Updated Author'
        }
        
        with app.app_context():
            updated_comment = CommentService.update_comment(sample_comment.id, update_data)
            assert updated_comment is not None
            assert updated_comment.content == update_data['content']
            assert updated_comment.author_name == update_data['author_name']
            assert updated_comment.id == sample_comment.id
            assert updated_comment.updated_at > sample_comment.updated_at
    
    def test_update_nonexistent_comment(self, app):
        """Test updating non-existent comment."""
        update_data = {'content': 'Updated content'}
        
        with app.app_context():
            result = CommentService.update_comment(999, update_data)
            assert result is None
    
    def test_update_comment_empty_content(self, app, sample_comment):
        """Test updating comment with empty content."""
        update_data = {'content': ''}
        
        with app.app_context():
            with pytest.raises(ValueError, match="Content cannot be empty"):
                CommentService.update_comment(sample_comment.id, update_data)
    
    def test_delete_comment_success(self, app, sample_comment):
        """Test successful comment deletion."""
        with app.app_context():
            success = CommentService.delete_comment(sample_comment.id)
            assert success is True
            
            # Verify comment is deleted
            deleted_comment = CommentService.get_comment_by_id(sample_comment.id)
            assert deleted_comment is None
    
    def test_delete_nonexistent_comment(self, app):
        """Test deleting non-existent comment."""
        with app.app_context():
            success = CommentService.delete_comment(999)
            assert success is False
    
    def test_validate_comment_data_creation(self):
        """Test comment data validation for creation."""
        # Valid data
        valid_data = {
            'content': 'Test comment',
            'author_name': 'Test User',
            'task_id': 1,
            'author_email': 'test@example.com'
        }
        
        result = CommentService.validate_comment_data(valid_data)
        assert result == valid_data
        
        # Missing required fields
        invalid_data = {'content': 'Test comment'}
        
        with pytest.raises(ValueError, match="Content and author_name are required"):
            CommentService.validate_comment_data(invalid_data)
        
        # Invalid email
        invalid_email_data = {
            'content': 'Test comment',
            'author_name': 'Test User',
            'task_id': 1,
            'author_email': 'invalid-email'
        }
        
        with pytest.raises(ValueError, match="Invalid email format"):
            CommentService.validate_comment_data(invalid_email_data)
    
    def test_validate_comment_data_update(self):
        """Test comment data validation for update."""
        # Valid update data
        valid_data = {'content': 'Updated content'}
        
        result = CommentService.validate_comment_data(valid_data, is_update=True)
        assert result == valid_data
        
        # No fields provided
        invalid_data = {}
        
        with pytest.raises(ValueError, match="At least one field must be provided"):
            CommentService.validate_comment_data(invalid_data, is_update=True)
        
        # Invalid email in update
        invalid_email_data = {'author_email': 'invalid-email'}
        
        with pytest.raises(ValueError, match="Invalid email format"):
            CommentService.validate_comment_data(invalid_email_data, is_update=True)
