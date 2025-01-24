# Task Manager API

## Overview

Task Manager API is designed for managing user authentication and task management operations.

## Base URL

[http://tm.0ps.tech/api](http://tm.0ps.tech/api)

## API Documentation

You can interact with the API on Swagger. Here’s the link to the Swagger Documentation for testing the available endpoints: [http://tm.0ps.tech/swagger](http://tm.0ps.tech/swagger)

## Authentication Endpoints

### Login

**POST** `/auth/login/`  
Authenticate and log in a user.

### Logout

**POST** `/auth/logout/`  
Log out a user and blacklist the token.

### Register

**POST** `/auth/register/`  
Register a new user.

### Token Refresh

**POST** `/auth/token/refresh/`  
Refresh access tokens using a refresh token.

## Task Management Endpoints

### List Tasks

**GET** `/tasks/`  
Retrieve all tasks with optional search filters.

### Create Task

**POST** `/tasks/`  
Create a new task.

### Retrieve Task

**GET** `/tasks/{id}/`  
Retrieve details of a specific task.

### Update Task

**PUT** `/tasks/{id}/`  
Update details of a specific task.

### Partially Update Task

**PATCH** `/tasks/{id}/`  
Partially update a specific task.

### Delete Task

**DELETE** `/tasks/{id}/`  
Delete a specific task.

## Definitions

### User Authentication

- **email**: string (required)
- **password**: string (required)

## Docker Setup Guide

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Hordunlarmy/TaskManagerAPI
cd TaskManagerAPI
```

### 2. Build the Docker Image

Once you're inside the project folder, build the Docker image:

```bash
docker compose up --build -d
```

### 3. Verify the Application

After the Docker image has been built successfully, you can verify the application by visiting [http://localhost:8000](http://localhost:8000) in your browser.
