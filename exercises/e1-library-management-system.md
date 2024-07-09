# Exercise 1: Library Management System

## Overview

In this project, you will build a backend system to manage a library's inventory of items, including books, magazines, DVDs, and music CDs. The system will handle borrowing and returning items, managing user memberships, and tracking user borrowing history. The project will be developed in steps to gradually add complexity and functionality.

You should focus on adhering to Object-Oriented Programming (OOP) principles and modularizing your application, so that extending it is easier.

## Step 1: Basic Borrowing and Returning Functionality

### User & Item Management

Before users can borrow or return items, they need to be added to the library system.

1. **Add a User**
    - Endpoint: `POST /users`
    - Request body should include:
        - `name` (string, required)
        - `email` (string, required)
        - `membership_type` (string, required; one of "student", "basic", "premium")
    - The system should generate a unique UUID for each user and return it in the response.
    - Example Request:
        
        ```json
        {
          "name": "John Doe",
          "email": "john.doe@example.com",
          "membership_type": "student"
        }
        ```
        
    - Example Response:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "name": "John Doe",
          "email": "john.doe@example.com",
          "membership_type": "student"
        }
        ```
        
2. Add an Item
- Endpoint: `POST /items`
- Request body should include:
    - `name` (string, required)
    - `type`(string, required; one of “book”, “dvd”, “magazine”)
- The system should generate a unique UUID for each item and return it in the response.
- Example Request:
    
    ```json
    {
      "name": "Madagascar",
      "type": "dvd",
    }
    ```
    
- Example Response:
    
    ```json
    {
      "item_id": "123e4567-e89b-12d3-a456-426614174020",
      "name": "Madagascar",
      "type": "dvd"
    }
    ```
    

> **Important Note:** you will need to store both users and items somehow. for the sake of the exercise, it doesn’t have to be a “real” database like sqlite, postgres, mongo, etc…
To keep it simple you can store the users and items in a runtime object, or write the data into a file - whatever you are more comfortable with.
> 

### Library Items

The library has the following items that can be borrowed:

- **Books**: Borrow for up to 3 months.
- **Magazines**: Borrow for up to 1 month.
- **DVDs**: Borrow for up to 1 month.

### Membership Types

There are three membership types in the library:

- **Student**
    - Can hold up to 5 books, 5 magazines, and 2 DVDs at a time.
- **Basic Membership**
    - Can hold up to 3 books, 3 magazines, and 2 DVDs at a time.
- **Premium Membership**
    - Can hold up to 10 books, 5 magazines, and 5 DVDs at a time.

### Borrowing and Returning Rules

- If a user tries to borrow a new item but already holds their limit per subscription type, the borrowing will fail (400 status code is expected to be returned).

### API Requirements

1. **Borrow an Item**
    - Endpoint: `POST /items/{id}/borrow`
    - Only authenticated users can borrow items.
    - Check the user’s membership type and current borrowed items before allowing borrowing.
    - Update the item’s status to "borrowed" and record the borrowing date.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "item_type": "book"
        }
        ```
        
2. **Return an Item**
    - Endpoint: `POST /items/{id}/return`
    - Only authenticated users can return items.
    - Update the item’s status to "available" and record the return date.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        ```
        
3. **User Borrowing History**
    - Endpoint: `GET /users/{id}/history`
    - Return a list of items borrowed by the user, including borrow and return dates.
    - Example Response:
        
        ```json
        [
          {
            "item_id": 1,
            "item_type": "book",
            "borrowed_date": "2023-01-01",
            "returned_date": "2023-02-01"
          },
          {
            "item_id": 2,
            "item_type": "dvd",
            "borrowed_date": "2023-03-01",
            "returned_date": "2023-03-15"
          }
        ]
        ```
        

## Step 2: Adding Music CDs

### New Library Item

The library now has music CDs that can be borrowed for up to 2 months.

### Membership Type Limits for CDs

- **Student**
    - Can hold up to 2 CDs at a time.
- **Basic Membership**
    - Can hold up to 2 CDs at a time.
- **Premium Membership**
    - Can hold up to 4 CDs at a time.

### API Extensions

1. **Borrow a CD**
    - Update the borrowing endpoint to handle CDs.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "item_type": "cd"
        }
        ```
        
2. **Return a CD**
    - Update the returning endpoint to handle CDs.
    - Example Request:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "item_type": "cd"
        }
        ```
        

## Step 3: Promotion System

### Promotion Rules

- Any user who has borrowed 15 or more books in the last year is eligible to hold double the number of books allowed by their membership type.
    - This applies to all membership types.

### API Extensions

1. **Check Promotion Eligibility**
    - Before allowing a user to borrow a book, check their borrowing history for the past year.
    - If they have borrowed 15 or more books, update their borrowing limit for books.
    - Example Logic:
        
        ```json
        {
          "user_id": "123e4567-e89b-12d3-a456-426614174000",
          "eligible_for_promotion": true,
          "new_book_limit": 20
        }
        ```
        

### Implementation Details

1. **Modify Borrowing Logic**
    - Adjust the borrowing logic to consider promotion eligibility for books.
    - Ensure that the new book limit is applied correctly for eligible users.

## Conclusion

By following these instructions, you will create a comprehensive Library Inventory Management System. Focus on adhering to OOP principles and modularizing your application to simulate real-world development practices. This project will help you develop practical backend skills and understand how to build and extend a real-world application.