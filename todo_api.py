from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for todos (in production, use a database)
todos = []

# Helper function to find todo by ID
def find_todo_by_id(todo_id):
    return next((todo for todo in todos if todo['id'] == todo_id), None)

# Helper function to validate todo data
def validate_todo_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['title']
    
    if not data:
        return False, "No data provided"
    
    for field in required_fields:
        if field not in data or not data[field].strip():
            return False, f"Missing or empty required field: {field}"
    
    return True, ""

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos with optional filtering"""
    # Optional query parameters for filtering
    status = request.args.get('status')
    
    filtered_todos = todos
    
    if status:
        if status.lower() not in ['pending', 'completed']:
            return jsonify({'error': 'Invalid status. Must be "pending" or "completed"'}), 400
        filtered_todos = [todo for todo in todos if todo['status'] == status.lower()]
    
    return jsonify({
        'todos': filtered_todos,
        'count': len(filtered_todos)
    })

@app.route('/api/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todo = find_todo_by_id(todo_id)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify(todo)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    # Validate required fields
    is_valid, error_message = validate_todo_data(data, ['title'])
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    # Create new todo
    new_todo = {
        'id': str(uuid.uuid4()),
        'title': data['title'].strip(),
        'description': data.get('description', '').strip(),
        'status': 'pending',  # Default status
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    todos.append(new_todo)
    
    return jsonify(new_todo), 201

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing todo"""
    todo = find_todo_by_id(todo_id)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({'error': 'Title cannot be empty'}), 400
        todo['title'] = data['title'].strip()
    
    if 'description' in data:
        todo['description'] = data['description'].strip()
    
    if 'status' in data:
        if data['status'].lower() not in ['pending', 'completed']:
            return jsonify({'error': 'Invalid status. Must be "pending" or "completed"'}), 400
        todo['status'] = data['status'].lower()
    
    todo['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify(todo)

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    todo = find_todo_by_id(todo_id)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    todos.remove(todo)
    
    return jsonify({'message': 'Todo deleted successfully'}), 200

@app.route('/api/todos/<todo_id>/toggle', methods=['PATCH'])
def toggle_todo_status(todo_id):
    """Toggle todo status between pending and completed"""
    todo = find_todo_by_id(todo_id)
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    # Toggle status
    todo['status'] = 'completed' if todo['status'] == 'pending' else 'pending'
    todo['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify(todo)

@app.route('/api/todos/bulk', methods=['DELETE'])
def delete_completed_todos():
    """Delete all completed todos"""
    global todos
    initial_count = len(todos)
    todos = [todo for todo in todos if todo['status'] != 'completed']
    deleted_count = initial_count - len(todos)
    
    return jsonify({
        'message': f'Deleted {deleted_count} completed todos',
        'deleted_count': deleted_count
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'total_todos': len(todos)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Add some sample data for testing
    sample_todos = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Learn Flask API development',
            'description': 'Build a comprehensive CRUD API with Flask',
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Write API documentation',
            'description': 'Document all the API endpoints and their usage',
            'status': 'completed',
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
    ]
    
    todos.extend(sample_todos)
    
    print("Starting Todo API server...")
    print("Available endpoints:")
    print("- GET /api/todos - Get all todos")
    print("- GET /api/todos/<id> - Get specific todo")
    print("- POST /api/todos - Create new todo")
    print("- PUT /api/todos/<id> - Update todo")
    print("- DELETE /api/todos/<id> - Delete todo")
    print("- PATCH /api/todos/<id>/toggle - Toggle todo status")
    print("- DELETE /api/todos/bulk - Delete all completed todos")
    print("- GET /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)