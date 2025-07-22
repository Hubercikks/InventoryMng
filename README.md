InventoryMng

InventoryMng is an inventory management system currently under development:
. It provides a RESTful API for managing products and users. The project is in an alpha stage – core functionality is being implemented
. In its current form, InventoryMng offers user account management and inventory endpoints, with plans for additional features (see Planned Features below).

Features
User management & authentication: Admin-level user creation, user login, and JWT-based authentication, product adding, updating, removing, listing.

Authentication

- POST /auth/login  
  Authenticate user and return a JWT access token.

- POST /auth/register  
  Register a new user account.  
  _Only admin users are allowed to create new users._


Product Management

- POST /api/products  
  Create a new product.  
  Requires authentication.

- DELETE /api/products/{product_id}
  Delete a product by its ID.  
  _Only admin users can delete products._

- PUT /api/products/{product_id} 
  Update a product by its ID.  
  You can update one or multiple fields of the product (partial updates supported).

- GET /api/list  
  Retrieve a list of all products.  
  Requires authentication.
 

Note: Future work includes audit logging, pdf generation, role-based access control (RBAC), and a user interface.

Technologies

This project is built with the following technologies:

  -Python 3.10
  
  -FastAPI (web framework)
  
  -SQLAlchemy (ORM)
  
  -PostgreSQL (database)
  
  -Docker (planned containerization)
  
Prerequisites

Python: Version 3.10 or higher is required.

Database: A PostgreSQL database instance (server) must be available.

Environment: Ensure the following environment variables are set:
SECRET_KEY – secret key for JWT signing.
URL_DATABASE – PostgreSQL connection string (e.g. postgresql://user:password@localhost/dbname)
ALGORITHM – JWT signing algorithm (e.g. HS256).

Installation

Clone the repository: 

    git clone https://github.com/Hubercikks/InventoryMng.git
    cd InventoryMng
    
Install dependencies:

    pip install -r requirements.txt
    
(This installs FastAPI, SQLAlchemy, and other required packages)
Configure environment: Create a .env file or otherwise export the required variables (see Prerequisites). For example:

    SECRET_KEY=your_secret_key
    URL_DATABASE=postgresql://user:password@localhost/dbname
    ALGORITHM=HS256

The database tables will be created automatically on first run (SQLAlchemy’s create_all is invoked in the app). Ensure your PostgreSQL server is running and the connection URL is correct.
Usage
After installation, start the FastAPI server. For example:

    uvicorn main:app --reload
    
By default, the API will be served at http://localhost:8000. You can then use the /auth and /api endpoints for user and product management. Interactive API documentation is available at http://localhost:8000/docs. For example, use the /auth/token endpoint to obtain a JWT token (logging in), then access protected routes or /me with the Authorization: Bearer <token> header.
