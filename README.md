# Flask REST API

This project implements a RESTful API using Flask for managing products and user authentication. It provides endpoints for registering users, logging in, creating, viewing, updating, and deleting products.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
## Endpoints

### User Registration

- **URL:** `/register`
- **Method:** `POST`
- **Data Params:**
  - `username`: User's username
  - `password`: User's password
- **Success Response:**
  - Code: `201`
  - Content: `{ "msg": "User registered successfully" }`
- **Error Response:**
  - Code: `400`
  - Content: `{ "msg": "Username and password required" }`

### User Login

- **URL:** `/login`
- **Method:** `POST`
- **Data Params:**
  - `username`: User's username
  - `password`: User's password
- **Success Response:**
  - Code: `200`
  - Content: `{ "access_token": "<token>" }`
- **Error Response:**
  - Code: `401`
  - Content: `{ "msg": "Wrong username or password" }`

### Product Management

- **URL:** `/products`
- **Method:** `POST`
- **Authentication:** Required
- **Data Params:**
  - `product_name`: Name of the product
  - `category`: Category of the product
  - `description`: Description of the product
  - `price`: Price of the product
- **Success Response:**
  - Code: `201`
  - Content: `{ "res": "<product_data>", "status": "201", "msg": "New product added!!!" }`
- **Error Response:**
  - Code: `404`
  - Content: `{ "res": "Error, a product with the same name already exists", "status": "404" }`


## Database

The application uses an SQLite database named `products.db` to store product and user information.

## Requirements

- Flask
- SQLAlchemy
- Flask-JWT-Extended

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

