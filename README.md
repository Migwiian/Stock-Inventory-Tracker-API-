# Stock Inventory Tracker API

A robust, secure, and feature-rich Django REST Framework (DRF) API for managing product inventory. This API provides full user authentication and allows users to perform CRUD operations on their inventory items while maintaining a complete audit log of all stock changes.

## 🚀 Features

- **User Authentication & Authorization**: Secure JWT-based authentication. Users can only access their own data.
- **Full CRUD Operations**: Create, read, update, and delete inventory items.
- **Advanced Filtering**: Filter items by category, price range (`price_min`, `price_max`), and low stock status (`low_stock=true`).
- **Audit Logging**: Every change to an item's quantity is automatically logged with the user, change type, amount, and timestamp.
- **Admin Interface**: Full access to data models through Django's built-in admin site.

## 📋 API Endpoints

| Endpoint | Method | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `/api/auth/register/` | POST | Register a new user | None |
| `/api/auth/token/` | POST | Obtain JWT access/refresh tokens | None |
| `/api/inventory/` | GET, POST | List all user's items or create a new item | Required |
| `/api/inventory/<id>/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a specific item | Required |
| `/api/inventory/<id>/history/` | GET | Retrieve the audit log for a specific item | Required |

### Filtering Inventory Items
Append query parameters to `GET /api/inventory/`:
- `?category=Electronics` - Filter by category (case-insensitive)
- `?price_min=10&price_max=100` - Filter by price range
- `?low_stock=true` - Show items with quantity less than 10

## 🛠️ Tech Stack

- **Backend Framework**: Django & Django REST Framework (DRF)
- **Authentication**: Simple JWT
- **Database**: SQLite (Development), PostgreSQL (Production-ready)
- **Package Management**: Pip

## 📦 Installation & Local Setup

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd Stock_Inventory_Tracker_API
    ```

2.  **Create and activate a virtual environment (Optional but recommended)**
    ```bash
    conda create -n inventory-env python=3.12.7
    conda activate inventory-env
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (to access the admin site)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.  
The Django admin site will be available at `http://127.0.0.1:8000/admin/`.

## 🔐 Authentication Flow

1.  **Register** a new user at `POST /api/auth/register/`.
2.  **Login** to obtain your tokens at `POST /api/auth/token/`. You will receive an `access` and a `refresh` token.
3.  **Use the access token** to authenticate all requests to protected endpoints. Include it in the `Authorization` header:
    ```
    Authorization: Bearer <your_access_token>
    ```

## 🗃️ Data Models

### InventoryItem
Stores the core product information.
- `name` (CharField)
- `quantity` (PositiveIntegerField)
- `price` (DecimalField)
- `category` (CharField)
- `user` (ForeignKey to CustomUser)
- `date_added` (DateTimeField, auto_now_add)
- `last_updated` (DateTimeField, auto_now)

### InventoryLog
Tracks every change to an item's quantity for auditing.
- `item` (ForeignKey to InventoryItem)
- `user` (ForeignKey to CustomUser)
- `change_type` (CharField with choices: `INITIAL`, `RESTOCK`, `SALE`)
- `quantity_changed` (IntegerField)
- `timestamp` (DateTimeField, auto_now_add)
- `notes` (TextField, optional)

## 🤝 Contributing

This is a portfolio project. Feel free to fork the repository and suggest improvements via pull requests.

## 📄 License

This project is licensed under the MIT License.
