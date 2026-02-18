# Inventory Location API

A robust REST API for managing inventory, locations, and stock movements. built with FastAPI and SQLAlchemy.

## Features

- **Items & Locations Management**: CRUD operations with soft delete support.
- **Inventory Tracking**: Real-time stock levels per item per location.
- **Transaction History**: Complete audit log of all stock movements (Inbound, Outbound, Adjustments).
- **Timestamps**: Automatic `created_at` and `updated_at` tracking.
- **Robust Architecture**:
  - Pydantic Settings for configuration.
  - SQLAlchemy ORM with relationships.
  - Clear separation of concerns (Routers, CRUD, Models, Schemas).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

3. Access generic API docs at: http://127.0.0.1:8000/docs

### Authentication
- **Secure Access**: All core endpoints now require JWT Authentication.
- **Register**: `POST /register` to create a new user.
- **Login**: `POST /token` (OAuth2 compatible) to get an access token.
- **Authorize**: Click "Authorize" in Swagger UI and input your token.

### Key Endpoints

#### Auth
- `POST /register`: Create account.
- `POST /token`: Login and get JWT.

#### Inventory Movement
`POST /inventory/movement`
- Use this endpoint to add or remove stock.
- `quantity`: Positive to add, negative to remove.
- `transaction_type`: "inbound", "outbound", or "adjustment".

### Transaction History
`GET /inventory/transactions`
- Filter by `item_id` or `location_id` to see history.

### Soft Deletes
- `DELETE /items/{id}` and `DELETE /locations/{id}` mark records as inactive instead of deleting execution.
