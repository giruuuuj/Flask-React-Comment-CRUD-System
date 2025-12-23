import pytest
import json
from app.models import Comment

class TestCommentRoutes:
    """Test cases for comment API routes."""
    
    def test_get_comments_by_task(self, client, sample_task, sample_comment):
        """Test getting all comments for a specific task."""
        response = client.get(f'/api/comments/?task_id={sample_task.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'comments' in data
        assert 'count' in data
        assert len(data['comments']) == 1
        assert data['comments'][0]['id'] == sample_comment.id
        assert data['comments'][0]['content'] == sample_comment.content
    
    def test_get_comments_no_task_id(self, client):
        """Test getting comments without providing task_id."""
        response = client.get('/api/comments/')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'task_id parameter is required' in data['error']
    
    def test_get_comments_nonexistent_task(self, client):
        """Test getting comments for a non-existent task."""
        response = client.get('/api/comments/?task_id=999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_create_comment_success(self, client, sample_task):
        """Test successful comment creation."""
        comment_data = {
            'content': 'New test comment',
            'author_name': 'New User',
            'author_email': 'newuser@example.com',
            'task_id': sample_task.id
        }
        
        response = client.post('/api/comments/', 
                             data=json.dumps(comment_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['content'] == comment_data['content']
        assert data['author_name'] == comment_data['author_name']
        assert data['task_id'] == sample_task.id
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_comment_missing_required_fields(self, client, sample_task):
        """Test creating comment with missing required fields."""
        # Missing content
        comment_data = {
            'author_name': 'Test User',
            'task_id': sample_task.id
        }
        
        response = client.post('/api/comments/', 
                             data=json.dumps(comment_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Content is required' in data['error']
    
    def test_create_comment_nonexistent_task(self, client):
        """Test creating comment for non-existent task."""
        comment_data = {
            'content': 'Test comment',
            'author_name': 'Test User',
            'task_id': 999
        }
        
        response = client.post('/api/comments/', 
                             data=json.dumps(comment_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        .assert 'not .not found' in data['error']
    
    def test_create_comment_invalid_email(self, client, sample_task):
        """Test creating comment with invalid email."""
        comment_data = {
            'content': 'Test comment',
            'author_name': 'Test User',
            'author_email': 'invalid-email',
            'task_id': sample_task.id
        }
        
        response = client.post('/api/comments/', 
                             data=json.dumps(comment_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid email format' in data['error']
    
    def test_get_comment_by_id(self, client, sample_comment):
        """Test getting a specific comment by ID."""
        response = client.get(f'/api/comments/{sample_comment.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_comment.id
        assert data['content'] == sample_comment.content
    
    def test_get_nonexistent_comment(self, client):
        """Test getting a non-existent comment."""
        response = client.get('/api/comments/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_update_comment_success(self, client, sample_comment):
        """Test successful comment update."""
        update_data = {
            'content': 'Updated comment content',
            'author_name': 'Updated Author'
        }
        
        response = client.put(f'/api/comments/{sample_comment.id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['content'] == update_data['content']
        assert data['author_name'] == update_data['author_name']
        assert data['id'] == sample_comment.id
    
    def test_update_comment_empty_content(self, client, sample_comment):
        """Test updating comment with empty content."""
        update_data = {
            'content': ''
        }
        
        response = client.put(f'/api/comments/{sample_comment.id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Content cannot be empty' in data['error']
    
    def test_update_nonexistent_comment(self, client):
        """Test updating a non-existent comment."""
        update_data = {
            'content': 'Updated content'
        }
        
        response = client.put('/api/comments/999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_delete_comment_success(self, client, sample_comment):
        """Test successful comment deletion."""
        response = client.delete(f'/api/comments/{sample_comment.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'deleted successfully' in data['message']
    
    def test_delete_nonexistent_comment(self, client):
        """Test deleting a non-existent comment."""
        response = client.delete('/api/comments/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_get_task_comments_alternative_endpoint(self, client, sample_task, sample_comment):
        """Test the alternative endpoint for getting task comments."""
        response = client.get(f'/api/comments/task/{sample_task.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'task_id' in data
        assert 'task_title' in data
        assert 'comments' in data
        assert 'count' in data
        assert data['task_id'] == sample_task.id
        assert data['task_title'] == sample_task.title
        assert len(data['comments']) == 1
    
    def test_create_comment_no_json(self, client):
        """Test creating comment without JSON data."""
        response = client.post('/api/comments/')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No JSON data provided' in data['error']
    
    def test_update_comment_no_json(self, client, sample_comment):
        """Test updating comment without JSON data."""
        response = client.put(f'/api/comments/{sample_comment.id}')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No JSON data provided' in data['error']
