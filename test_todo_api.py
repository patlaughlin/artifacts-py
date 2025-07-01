#!/usr/bin/env python3
"""
Test script for the TODO API
Tests all CRUD endpoints and validates responses
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Make sure it's running on port 5000")
        return False
    return True

def test_get_all_todos():
    """Test getting all todos"""
    print("\nTesting GET all todos...")
    response = requests.get(f"{BASE_URL}/todos")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ GET all todos passed. Found {data['count']} todos")
        return data['todos']
    else:
        print(f"❌ GET all todos failed with status: {response.status_code}")
        return []

def test_create_todo():
    """Test creating a new todo"""
    print("\nTesting POST new todo...")
    new_todo = {
        "title": "Test Todo from API Test",
        "description": "This is a test todo created via API test"
    }
    
    response = requests.post(f"{BASE_URL}/todos", json=new_todo)
    if response.status_code == 201:
        todo = response.json()
        print(f"✅ POST new todo passed. Created todo with ID: {todo['id']}")
        return todo
    else:
        print(f"❌ POST new todo failed with status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_get_single_todo(todo_id):
    """Test getting a single todo by ID"""
    print(f"\nTesting GET single todo with ID: {todo_id}")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code == 200:
        todo = response.json()
        print(f"✅ GET single todo passed. Title: {todo['title']}")
        return todo
    else:
        print(f"❌ GET single todo failed with status: {response.status_code}")
        return None

def test_update_todo(todo_id):
    """Test updating a todo"""
    print(f"\nTesting PUT update todo with ID: {todo_id}")
    update_data = {
        "title": "Updated Test Todo",
        "description": "This todo has been updated via API test",
        "status": "completed"
    }
    
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    if response.status_code == 200:
        todo = response.json()
        print(f"✅ PUT update todo passed. New title: {todo['title']}, Status: {todo['status']}")
        return todo
    else:
        print(f"❌ PUT update todo failed with status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_toggle_todo_status(todo_id):
    """Test toggling todo status"""
    print(f"\nTesting PATCH toggle status for todo ID: {todo_id}")
    response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle")
    if response.status_code == 200:
        todo = response.json()
        print(f"✅ PATCH toggle status passed. New status: {todo['status']}")
        return todo
    else:
        print(f"❌ PATCH toggle status failed with status: {response.status_code}")
        return None

def test_filter_todos():
    """Test filtering todos by status"""
    print("\nTesting GET todos with status filter...")
    
    # Test filtering by pending
    response = requests.get(f"{BASE_URL}/todos?status=pending")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Filter by 'pending' passed. Found {data['count']} pending todos")
    else:
        print(f"❌ Filter by 'pending' failed with status: {response.status_code}")
    
    # Test filtering by completed
    response = requests.get(f"{BASE_URL}/todos?status=completed")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Filter by 'completed' passed. Found {data['count']} completed todos")
    else:
        print(f"❌ Filter by 'completed' failed with status: {response.status_code}")

def test_delete_todo(todo_id):
    """Test deleting a todo"""
    print(f"\nTesting DELETE todo with ID: {todo_id}")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code == 200:
        print("✅ DELETE todo passed")
        return True
    else:
        print(f"❌ DELETE todo failed with status: {response.status_code}")
        return False

def test_error_cases():
    """Test various error cases"""
    print("\nTesting error cases...")
    
    # Test GET non-existent todo
    response = requests.get(f"{BASE_URL}/todos/non-existent-id")
    if response.status_code == 404:
        print("✅ GET non-existent todo returns 404 as expected")
    else:
        print(f"❌ GET non-existent todo should return 404, got {response.status_code}")
    
    # Test POST with missing title
    response = requests.post(f"{BASE_URL}/todos", json={"description": "No title"})
    if response.status_code == 400:
        print("✅ POST without title returns 400 as expected")
    else:
        print(f"❌ POST without title should return 400, got {response.status_code}")
    
    # Test UPDATE non-existent todo
    response = requests.put(f"{BASE_URL}/todos/non-existent-id", json={"title": "Test"})
    if response.status_code == 404:
        print("✅ PUT non-existent todo returns 404 as expected")
    else:
        print(f"❌ PUT non-existent todo should return 404, got {response.status_code}")

def main():
    """Run all API tests"""
    print("=" * 50)
    print("TODO API Test Suite")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ Cannot connect to API server. Exiting...")
        return
    
    # Test getting initial todos
    initial_todos = test_get_all_todos()
    
    # Test creating a new todo
    new_todo = test_create_todo()
    if not new_todo:
        print("\n❌ Cannot create todos. Exiting...")
        return
    
    todo_id = new_todo['id']
    
    # Test getting the created todo
    test_get_single_todo(todo_id)
    
    # Test updating the todo
    test_update_todo(todo_id)
    
    # Test toggling status
    test_toggle_todo_status(todo_id)
    
    # Test filtering
    test_filter_todos()
    
    # Test error cases
    test_error_cases()
    
    # Test deleting the todo
    test_delete_todo(todo_id)
    
    # Final check
    final_todos = test_get_all_todos()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Initial todos: {len(initial_todos)}")
    print(f"Final todos: {len(final_todos)}")
    print("=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()