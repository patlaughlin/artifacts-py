# TODO API Documentation

A comprehensive RESTful API for managing todos with full CRUD (Create, Read, Update, Delete) operations.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python todo_api.py
   ```

3. **Test the API:**
   ```bash
   python test_todo_api.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Base URL
```
http://localhost:5000/api
```

### 1. Health Check
**GET** `/health`

Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T10:30:00.000000",
  "total_todos": 2
}
```

### 2. Get All Todos
**GET** `/todos`

Retrieve all todos with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (`pending` or `completed`)

**Examples:**
```bash
# Get all todos
curl http://localhost:5000/api/todos

# Get only pending todos
curl http://localhost:5000/api/todos?status=pending

# Get only completed todos
curl http://localhost:5000/api/todos?status=completed
```

**Response:**
```json
{
  "todos": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Learn Flask API development",
      "description": "Build a comprehensive CRUD API with Flask",
      "status": "pending",
      "created_at": "2025-01-27T10:00:00.000000",
      "updated_at": "2025-01-27T10:00:00.000000"
    }
  ],
  "count": 1
}
```

### 3. Get Single Todo
**GET** `/todos/{id}`

Retrieve a specific todo by its ID.

**Example:**
```bash
curl http://localhost:5000/api/todos/123e4567-e89b-12d3-a456-426614174000
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Flask API development",
  "description": "Build a comprehensive CRUD API with Flask",
  "status": "pending",
  "created_at": "2025-01-27T10:00:00.000000",
  "updated_at": "2025-01-27T10:00:00.000000"
}
```

**Error Response (404):**
```json
{
  "error": "Todo not found"
}
```

### 4. Create New Todo
**POST** `/todos`

Create a new todo item.

**Request Body:**
```json
{
  "title": "New Todo Item",
  "description": "Optional description"
}
```

**Required Fields:**
- `title`: String (required, cannot be empty)

**Optional Fields:**
- `description`: String (defaults to empty string)

**Example:**
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, and eggs"
  }'
```

**Response (201 Created):**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "title": "Buy groceries",
  "description": "Milk, bread, and eggs",
  "status": "pending",
  "created_at": "2025-01-27T10:15:00.000000",
  "updated_at": "2025-01-27T10:15:00.000000"
}
```

**Error Response (400):**
```json
{
  "error": "Missing or empty required field: title"
}
```

### 5. Update Todo
**PUT** `/todos/{id}`

Update an existing todo item.

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed"
}
```

**Optional Fields:**
- `title`: String (cannot be empty if provided)
- `description`: String
- `status`: String (`pending` or `completed`)

**Example:**
```bash
curl -X PUT http://localhost:5000/api/todos/456e7890-e89b-12d3-a456-426614174001 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries - DONE",
    "status": "completed"
  }'
```

**Response (200 OK):**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "title": "Buy groceries - DONE",
  "description": "Milk, bread, and eggs",
  "status": "completed",
  "created_at": "2025-01-27T10:15:00.000000",
  "updated_at": "2025-01-27T10:25:00.000000"
}
```

### 6. Toggle Todo Status
**PATCH** `/todos/{id}/toggle`

Toggle a todo's status between `pending` and `completed`.

**Example:**
```bash
curl -X PATCH http://localhost:5000/api/todos/456e7890-e89b-12d3-a456-426614174001/toggle
```

**Response (200 OK):**
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "title": "Buy groceries - DONE",
  "description": "Milk, bread, and eggs",
  "status": "pending",
  "created_at": "2025-01-27T10:15:00.000000",
  "updated_at": "2025-01-27T10:30:00.000000"
}
```

### 7. Delete Todo
**DELETE** `/todos/{id}`

Delete a specific todo item.

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/todos/456e7890-e89b-12d3-a456-426614174001
```

**Response (200 OK):**
```json
{
  "message": "Todo deleted successfully"
}
```

### 8. Delete All Completed Todos
**DELETE** `/todos/bulk`

Delete all todos with status `completed`.

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/todos/bulk
```

**Response (200 OK):**
```json
{
  "message": "Deleted 3 completed todos",
  "deleted_count": 3
}
```

## Todo Object Schema

Each todo object has the following structure:

```json
{
  "id": "string (UUID)",
  "title": "string (required)",
  "description": "string (optional)",
  "status": "string (pending|completed)",
  "created_at": "string (ISO timestamp)",
  "updated_at": "string (ISO timestamp)"
}
```

## HTTP Status Codes

- `200 OK`: Successful GET, PUT, PATCH, or DELETE
- `201 Created`: Successful POST (todo created)
- `400 Bad Request`: Invalid request data or missing required fields
- `404 Not Found`: Todo not found or invalid endpoint
- `500 Internal Server Error`: Server error

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Description of the error"
}
```

## CORS Support

The API includes CORS (Cross-Origin Resource Sharing) support, allowing frontend applications from different domains to access the API.

## Data Storage

The current implementation uses in-memory storage. In a production environment, you would typically:

1. Replace the in-memory storage with a database (PostgreSQL, MongoDB, etc.)
2. Add authentication and authorization
3. Implement pagination for large datasets
4. Add rate limiting and other security measures

## Testing

Use the provided test script to verify all functionality:

```bash
python test_todo_api.py
```

The test script will:
- Check API connectivity
- Test all CRUD operations
- Validate error handling
- Verify filtering functionality

## Example Usage Scenarios

### 1. Create a shopping list
```bash
# Create todos for shopping
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2% milk, 1 gallon"}'

curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy bread", "description": "Whole wheat bread"}'
```

### 2. Mark items as completed
```bash
# Toggle status to completed
curl -X PATCH http://localhost:5000/api/todos/{todo-id}/toggle
```

### 3. Clean up completed tasks
```bash
# Delete all completed todos
curl -X DELETE http://localhost:5000/api/todos/bulk
```

### 4. Get progress overview
```bash
# Get pending todos
curl http://localhost:5000/api/todos?status=pending

# Get completed todos  
curl http://localhost:5000/api/todos?status=completed
```

This API provides a solid foundation for any todo or task management application!