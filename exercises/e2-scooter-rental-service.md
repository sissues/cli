# Scooter Rental Service

### Overview

In this project, you will build a backend system to manage a scooter rental service. The system will handle scooter reservations, starting and ending rides, user management, and ride history tracking. The project will be developed in steps to gradually add complexity and functionality.

## Step 1: Basic Reservation and Ride Functionality

### User Management

Before users can reserve or start a ride, they need to be added to the scooter rental system.

1. **Add a User**
    - Endpoint: `POST /users`
    - Request body should include:
        - `name` (string, required)
        - `email` (string, required)
        - `membership_type` (string, required; one of "basic", "premium")
    - The system should generate a unique UUID for each user and return it in the response.
    - Example Request:
        
        ```json
        {
          "name": "John Doe",
          "email": "john.doe@example.com",
          "membership_type": "basic"
        }
        ```
        
    - Example Response:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "name": "John Doe",
          "email": "john.doe@example.com",
          "membership_type": "basic"
        }
        ```
        

### Scooter Management

1. **Add a Scooter**
    - Endpoint: `POST /scooters`
    - Request body should include:
        - `location` (string, required)
        - `status` (string, required; one of "available", "reserved", "in_use", "maintenance")
    - The system should generate a unique ID for each scooter and return it in the response.
    - Example Request:
        
        ```json
        {
          "location": "Downtown",
          "status": "available"
        }
        ```
        
    - Example Response:
        
        ```json
        {
          "scooter_id": "S123456",
          "location": "Downtown",
          "status": "available"
        }
        ```
        

### Reservation and Ride Rules

- Users can reserve an available scooter.
- Users can start a ride on a reserved scooter.
- Users can end a ride and make the scooter available again.

### API Requirements

1. **Reserve a Scooter**
    - Endpoint: `POST /scooters/{id}/reserve`
    - Only authenticated users can reserve scooters.
    - Update the scooter’s status to "reserved" and record the reservation time.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
        
2. **Start a Ride**
    - Endpoint: `POST /scooters/{id}/start`
    - Only authenticated users can start a ride on a reserved scooter.
    - Update the scooter’s status to "in_use" and record the start time.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
        
3. **End a Ride**
    - Endpoint: `POST /scooters/{id}/end`
    - Only authenticated users can end a ride.
    - Update the scooter’s status to "available", record the end time, and calculate the ride duration.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
        
4. **User Ride History**
    - Endpoint: `GET /users/{id}/history`
    - Return a list of rides taken by the user, including start and end times and duration.
    - Example Response:
        
        ```json
        [
          {
            "scooter_id": "123e4567-e89b-12d3-a456-426614174001",
            "start_time": "2023-01-01T10:00:00Z",
            "end_time": "2023-01-01T10:30:00Z",
            "duration": 30
          },
          {
            "scooter_id": "123e4567-e89b-12d3-a456-426614174002",
            "start_time": "2023-02-01T11:00:00Z",
            "end_time": "2023-02-01T11:45:00Z",
            "duration": 45
          }
        ]
        ```
        

## Step 2: Advanced Features

### Membership Benefits

1. **Membership Levels**
    - **Basic Membership**
        - Pay-per-ride pricing.
    - **Premium Membership**
        - Monthly subscription with unlimited rides up to 60 minutes each.
        - Additional charges apply for rides longer than 60 minutes.
2. **Pricing System**
    - Implement a pricing system based on membership type and ride duration.
    - Calculate the cost of each ride and update the user’s account accordingly.

### API Extensions

1. **Calculate Ride Cost**
    - Endpoint: `GET /scooters/{id}/cost`
    - Calculate the cost of a ride based on the membership type and ride duration.
    - Example Response:
        
        ```json
        {
          "ride_cost": 5.00
        }
        ```
        
2. **Payment Integration**
    - Integrate with a payment gateway to handle ride payments.
    - Update user’s account balance and transaction history.

## Step 3: Promotion and Reward System

### Promotion Rules

1. **Ride Rewards**
    - Implement a reward system where users earn points for each ride.
    - Points can be redeemed for discounts or free rides.

### API Extensions

1. **Reward Points**
    - Endpoint: `GET /users/{id}/rewards`
    - Return the user’s current reward points and reward history.
    - Example Response:
        
        ```json
        {
          "current_points": 120,
          "reward_history": [
            {
              "ride_id": "123e4567-e89b-12d3-a456-426614174003",
              "points_earned": 10,
              "date": "2023-01-01"
            },
            {
              "ride_id": "123e4567-e89b-12d3-a456-426614174004",
              "points_earned": 15,
              "date": "2023-02-01"
            }
          ]
        }
        ```
        
2. **Redeem Rewards**
    - Endpoint: `POST /users/{id}/rewards/redeem`
    - Redeem points for discounts or free rides.
    - Update the user’s reward points and transaction history.
    - Example Request:
        
        ```json
        {
          "points_to_redeem": 50
        }
        ```
        

## Conclusion

By following these instructions, you will create a comprehensive Scooter Rental Service system. Focus on adhering to OOP principles and modularizing your application to simulate real-world development practices. This project will help you develop practical backend skills and understand how to build and extend a real-world application with advanced features and integrations.