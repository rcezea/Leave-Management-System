# Leave-Management-System
Webstack - Portfolio Project

### Authentication and User Management

#### User Registration
- **Endpoint**: `POST /auth/register`
- **Description**: Register a new user (employee or admin).

  - **Input Data**:
    - `username` (string, required)
    - `password` (string, required)
    - `email` (string, required)
    - `role` (string, required, e.g., 'employee' or 'admin')

  - **Format**: JSON
    ```json
    {
      "username": "john_doe",
      "password": "securepassword123",
      "email": "john@example.com",
      "role": "employee"
    }
    ```

  - **Output Data**:
    - `message` (string)
    - `user_id` (string)

  - **Format**: JSON
    ```json
    {
      "message": "User registered successfully",
      "user_id": "60f7cae51c4ae45d3c5f3a1b"
    }
    ```

  - **Errors**:
    - Raise error if any field is missing or invalid.
    - Raise error if the email or username already exists.
    - Return 400 status code for validation errors.

#### User Login
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticate and log in a user.

  - **Input Data**:
    - `username` (string, required)
    - `password` (string, required)

  - **Format**: JSON
    ```json
    {
      "username": "john_doe",
      "password": "securepassword123"
    }
    ```

  - **Output Data**:
    - `message` (string)
    - `token` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Login successful",
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

  - **Errors**:
    - Raise error if username or password is incorrect.
    - Return 401 status code for authentication errors.

#### User Logout
- **Endpoint**: `POST /auth/logout`
- **Description**: Log out the current user.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Logout successful"
    }
    ```

  - **Errors**:
    - Raise error if the user is not logged in.
    - Return 401 status code for authentication errors.

#### Password Reset Request
- **Endpoint**: `POST /auth/password-reset`
- **Description**: Request a password reset link.

  - **Input Data**:
    - `email` (string, required)

  - **Format**: JSON
    ```json
    {
      "email": "john@example.com"
    }
    ```

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Password reset link sent"
    }
    ```

  - **Errors**:
    - Raise error if the email is not found.
    - Return 404 status code for not found errors.

#### Password Reset
- **Endpoint**: `POST /auth/password-reset/<token>`
- **Description**: Reset password using the provided token.

  - **Input Data**:
    - `new_password` (string, required)

  - **Format**: JSON
    ```json
    {
      "new_password": "newsecurepassword123"
    }
    ```

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Password reset successful"
    }
    ```

  - **Errors**:
    - Raise error if the token is invalid or expired.
    - Raise error if the new password does not meet security criteria.
    - Return 400 status code for validation errors.

### Employee Endpoints

#### Apply for Leave
- **Endpoint**: `POST /leave/apply`
- **Description**: Submit a new leave application.

  - **Input Data**:
    - `leave_type` (string, required)
    - `start_date` (string, required, format: YYYY-MM-DD)
    - `end_date` (string, required, format: YYYY-MM-DD)
    - `reason` (string, required)

  - **Format**: JSON
    ```json
    {
      "leave_type": "sick",
      "start_date": "2024-07-01",
      "end_date": "2024-07-05",
      "reason": "Medical treatment"
    }
    ```

  - **Output Data**:
    - `message` (string)
    - `leave_id` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave application submitted",
      "leave_id": "60f7cae51c4ae45d3c5f3a1c"
    }
    ```

  - **Errors**:
    - Raise error if any field is missing or invalid.
    - Raise error if the leave dates overlap with existing approved leaves.
    - Return 400 status code for validation errors.

#### View Leave Status
- **Endpoint**: `GET /leave/status`
- **Description**: View the status of all leave applications submitted by the user.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `leave_applications` (array of objects)
      - Each object contains:
        - `leave_id` (string)
        - `leave_type` (string)
        - `start_date` (string, format: YYYY-MM-DD)
        - `end_date` (string, format: YYYY-MM-DD)
        - `reason` (string)
        - `status` (string, e.g., 'pending', 'approved', 'rejected')

  - **Format**: JSON
    ```json
    {
      "leave_applications": [
        {
          "leave_id": "60f7cae51c4ae45d3c5f3a1c",
          "leave_type": "sick",
          "start_date": "2024-07-01",
          "end_date": "2024-07-05",
          "reason": "Medical treatment",
          "status": "pending"
        }
      ]
    }
    ```

  - **Errors**:
    - Raise error if the user is not authenticated.
    - Return 401 status code for authentication errors.

#### Cancel Leave Application
- **Endpoint**: `DELETE /leave/cancel/<leave_id>`
- **Description**: Cancel a pending leave application.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave application cancelled"
    }
    ```

  - **Errors**:
    - Raise error if the leave application is not found or is not in a cancellable state (e.g., already approved).
    - Return 404 status code for not found errors.

### Manager/Admin Endpoints

#### View Leave Applications
- **Endpoint**: `GET /admin/leave-applications`
- **Description**: View all leave applications submitted by employees.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `leave_applications` (array of objects)
      - Each object contains:
        - `leave_id` (string)
        - `user_id` (string)
        - `leave_type` (string)
        - `start_date` (string, format: YYYY-MM-DD)
        - `end_date` (string, format: YYYY-MM-DD)
        - `reason` (string)
        - `status` (string, e.g., 'pending', 'approved', 'rejected')

  - **Format**: JSON
    ```json
    {
      "leave_applications": [
        {
          "leave_id": "60f7cae51c4ae45d3c5f3a1c",
          "user_id": "60f7cae51c4ae45d3c5f3a1b",
          "leave_type": "sick",
          "start_date": "2024-07-01",
          "end_date": "2024-07-05",
          "reason": "Medical treatment",
          "status": "pending"
        }
      ]
    }
    ```

  - **Errors**:
    - Raise error if the user is not authenticated or does not have admin privileges.
    - Return 401 status code for authentication errors.

#### Approve Leave
- **Endpoint**: `PUT /admin/approve-leave/<leave_id>`
- **Description**: Approve a leave application.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave application approved"
    }
    ```

  - **Errors**:
    - Raise error if the leave application is not found or is not in a pending state.
    -

 Return 404 status code for not found errors.

#### Reject Leave
- **Endpoint**: `PUT /admin/reject-leave/<leave_id>`
- **Description**: Reject a leave application.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave application rejected"
    }
    ```

  - **Errors**:
    - Raise error if the leave application is not found or is not in a pending state.
    - Return 404 status code for not found errors.

#### View Employee Leave History
- **Endpoint**: `GET /admin/employee-leave-history/<employee_id>`
- **Description**: View the leave history of a specific employee.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `leave_history` (array of objects)
      - Each object contains:
        - `leave_id` (string)
        - `leave_type` (string)
        - `start_date` (string, format: YYYY-MM-DD)
        - `end_date` (string, format: YYYY-MM-DD)
        - `reason` (string)
        - `status` (string, e.g., 'pending', 'approved', 'rejected')

  - **Format**: JSON
    ```json
    {
      "leave_history": [
        {
          "leave_id": "60f7cae51c4ae45d3c5f3a1c",
          "leave_type": "sick",
          "start_date": "2024-07-01",
          "end_date": "2024-07-05",
          "reason": "Medical treatment",
          "status": "approved"
        }
      ]
    }
    ```

  - **Errors**:
    - Raise error if the employee is not found.
    - Return 404 status code for not found errors.

### Common Endpoints

#### View Leave Types
- **Endpoint**: `GET /leave/types`
- **Description**: Retrieve a list of available leave types (e.g., sick leave, annual leave).

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `leave_types` (array of objects)
      - Each object contains:
        - `type_id` (string)
        - `name` (string)

  - **Format**: JSON
    ```json
    {
      "leave_types": [
        {
          "type_id": "1",
          "name": "Sick Leave"
        },
        {
          "type_id": "2",
          "name": "Annual Leave"
        }
      ]
    }
    ```

  - **Errors**: None expected.

#### View Leave Balance
- **Endpoint**: `GET /leave/balance`
- **Description**: View the remaining leave balance for the current user.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `leave_balance` (object)
      - Each key-value pair represents a leave type and its remaining balance.
      - `sick_leave` (integer)
      - `annual_leave` (integer)

  - **Format**: JSON
    ```json
    {
      "leave_balance": {
        "sick_leave": 5,
        "annual_leave": 10
      }
    }
    ```

  - **Errors**:
    - Raise error if the user is not authenticated.
    - Return 401 status code for authentication errors.

#### Dashboard Statistics
- **Endpoint**: `GET /dashboard/stats`
- **Description**: View statistics and summary data for leaves (e.g., total leaves taken, pending applications).

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `stats` (object)
      - `total_leaves` (integer)
      - `pending_leaves` (integer)
      - `approved_leaves` (integer)
      - `rejected_leaves` (integer)

  - **Format**: JSON
    ```json
    {
      "stats": {
        "total_leaves": 20,
        "pending_leaves": 3,
        "approved_leaves": 15,
        "rejected_leaves": 2
      }
    }
    ```

  - **Errors**: None expected.

### Optional/Additional Endpoints

#### Update User Profile
- **Endpoint**: `PUT /user/profile`
- **Description**: Update user profile information.

  - **Input Data**:
    - `username` (string, optional)
    - `email` (string, optional)
    - `password` (string, optional)

  - **Format**: JSON
    ```json
    {
      "username": "john_doe_updated",
      "email": "john_updated@example.com",
      "password": "newpassword123"
    }
    ```

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Profile updated successfully"
    }
    ```

  - **Errors**:
    - Raise error if any field is invalid.
    - Raise error if the email or username already exists.
    - Return 400 status code for validation errors.

#### Admin Dashboard
- **Endpoint**: `GET /admin/dashboard`
- **Description**: View admin-specific dashboard data and statistics.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `dashboard_data` (object)
      - `total_users` (integer)
      - `total_leaves` (integer)
      - `pending_leaves` (integer)

  - **Format**: JSON
    ```json
    {
      "dashboard_data": {
        "total_users": 50,
        "total_leaves": 100,
        "pending_leaves": 5
      }
    }
    ```

  - **Errors**: None expected.

#### Notifications
- **Endpoint**: `GET /notifications`
- **Description**: Retrieve notifications for the current user.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `notifications` (array of objects)
      - Each object contains:
        - `notification_id` (string)
        - `message` (string)
        - `read` (boolean)

  - **Format**: JSON
    ```json
    {
      "notifications": [
        {
          "notification_id": "1",
          "message": "Your leave application has been approved",
          "read": false
        }
      ]
    }
    ```

  - **Errors**: None expected.

#### Admin Create Leave Type
- **Endpoint**: `POST /admin/leave-type`
- **Description**: Create a new type of leave (e.g., paternity leave).

  - **Input Data**:
    - `name` (string, required)

  - **Format**: JSON
    ```json
    {
      "name": "Paternity Leave"
    }
    ```

  - **Output Data**:
    - `message` (string)
    - `type_id` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave type created successfully",
      "type_id": "3"
    }
    ```

  - **Errors**:
    - Raise error if the name is missing or already exists.
    - Return 400 status code for validation errors.

#### Admin Update Leave Type
- **Endpoint**: `PUT /admin/leave-type/<type_id>`
- **Description**: Update an existing leave type.

  - **Input Data**:
    - `name` (string, optional)

  - **Format**: JSON
    ```json
    {
      "name": "Updated Leave Type Name"
    }
    ```

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave type updated successfully"
    }
    ```

  - **Errors**:
    - Raise error if the type_id is not found.
    - Raise error if the name already exists.
    - Return 400 status code for validation errors.

#### Admin Delete Leave Type
- **Endpoint**: `DELETE /admin/leave-type/<type_id>`
- **Description**: Delete an existing leave type.

  - **Input Data**: None
  - **Format**: N/A

  - **Output Data**:
    - `message` (string)

  - **Format**: JSON
    ```json
    {
      "message": "Leave type deleted successfully"
    }
    ```

  - **Errors**:
    - Raise error if the type_id is not found.
    - Return 404 status code for not found errors.
