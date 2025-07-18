📦 InventoryMng
InventoryMng is an inventory management system currently under development.

🚧 Status
Alpha Stage — Core functionality is being implemented.

✅ Implemented:

User creation

User login

JWT-based authentication

/me endpoint to test token-based user retrieval

🔮 Planned Features

  🔒 Improve authentication & security logic

  📦 Endpoints for product creation, update, and deletion

  🧾 Audit logging for all product changes

  🛡️ Role-based access control with privileges

  💻 Frontend interface

  🧹 Code and architecture cleanup

  🐳 Docker support for containerization

🛠️ Technologies Used
  
  Python 3.10

  FastAPI

  SQLAlchemy

  PostgreSQL

  Docker (planned)

🚀 Getting Started

  1. Install dependencies
   
    pip install -r requirements.txt
  
  3. Set up environment variables
   
  Create and configure a .env file or set the following manually:

  SECRET_KEY — for JWT token signing

  DATABASE_URL — PostgreSQL connection string (e.g., postgresql://user:pass@localhost/dbname)
