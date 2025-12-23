"""Database initialization script for MySQL"""
import pymysql
from app import create_app, db
from app.models import Task, Comment

def create_mysql_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_comment_db")
        cursor.execute("USE task_comment_db")
        
        print("MySQL database 'task_comment_db' created or already exists")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating MySQL database: {e}")
        return False
    
    return True

def create_tables():
    """Create tables using Flask-SQLAlchemy"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Create sample data
            if not Task.query.first():
                sample_task = Task(
                    title="Sample Task",
                    description="This is a sample task to test the system",
                    status="pending",
                    priority="medium"
                )
                db.session.add(sample_task)
                db.session.commit()
                
                sample_comment = Comment(
                    content="This is a sample comment",
                    author_name="Test User",
                    author_email="test@example.com",
                    task_id=sample_task.id
                )
                db.session.add(sample_comment)
                db.session.commit()
                
                print("Sample data created!")
            
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("Initializing MySQL database...")
    
    # Step 1: Create database
    if create_mysql_database():
        # Step 2: Create tables
        if create_tables():
            print("Database initialization complete!")
        else:
            print("Failed to create tables")
    else:
        print("Failed to create database")
