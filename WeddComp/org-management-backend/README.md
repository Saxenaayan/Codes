

---

# 📘 **(FINAL VERSION)**

---

# **Organization Management Backend (FastAPI + MongoDB + JWT + Automated Tests)**

A scalable, modular **multi-tenant backend system** designed to dynamically create and manage organizations, along with secure admin authentication and per-organization isolated collections.

This project includes:

✔ FastAPI backend
✔ MongoDB master database + dynamic collections
✔ JWT-based admin authentication
✔ Fully automated test suite using **pytest + mongomock**
✔ Clean, class-based architecture

---

#  **Features**

### 🔹 **Multi-Tenant Architecture**

Each organization gets its own MongoDB collection automatically:

```
orgs/
  ├── org_companyA
  ├── org_companyB
  └── org_testorg
```

###  **Master Database**

Stores:

* Organization metadata
* Admin user accounts
* Dynamic collection links

###  **Secure Authentication**

* Password hashing using bcrypt (Passlib)
* JWT tokens with admin + org identifiers

### **REST API Endpoints**

* `POST /org/create`
* `GET /org/get`
* `PUT /org/update`
* `DELETE /org/delete`
* `POST /admin/login`

### **Automated Tests Included**

* 5 test files
* Runs with NoDB using **mongomock**
* Fast, isolated, and CI/CD friendly

---

# **Tech Stack**

| Component      | Technology        |
| -------------- | ----------------- |
| Backend        | FastAPI           |
| Database       | MongoDB           |
| Password Hash  | bcrypt            |
| Authentication | JWT               |
| Testing        | pytest, mongomock |
| Language       | Python            |

---

#  **Project Structure**

```
app/
 ├── main.py
 ├── config.py
 ├── database.py
 ├── utils/
 │    ├── security.py
 │    └── jwt_handler.py
 ├── models/
 │    ├── organization.py
 │    └── admin.py
 ├── services/
 │    ├── org_service.py
 │    └── auth_service.py
 └── routes/
      ├── org_routes.py
      └── auth_routes.py

tests/
 ├── conftest.py
 ├── test_1_create_org.py
 ├── test_2_login.py
 ├── test_3_get_org.py
 ├── test_4_update_org.py
 └── test_5_delete_org.py
```

---

#  **Installation & Setup**

## 1️⃣ Clone the repository

```
git clone <your-github-repo>
cd org-management-backend
```

---

## 2️⃣ Install backend dependencies

```
pip install -r requirements.txt
```

---

## 3️⃣ Create `.env` file or configure environment variables

```
MONGO_URL=mongodb://localhost:27017
JWT_SECRET=your_secret_key
```

---

## 4️⃣ Start the FastAPI server

```
uvicorn app.main:app --reload
```

You should now see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

#  **API Documentation**

FastAPI auto-generates interactive API docs:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

#  **Automated Testing (Pytest + mongomock)**

### ✔ No real MongoDB needed

The test suite uses **mongomock**, which simulates MongoDB in memory.

### ✔ Run tests easily

### 1️⃣ Install test dependencies

```
pip install -r requirements-tests.txt
```

### 2️⃣ Run the tests

```
pytest -v
```

### 3️⃣ Expected output

```
test_1_create_org.py::test_create_org PASSED
test_2_login.py::test_admin_login PASSED
test_3_get_org.py::test_get_org PASSED
test_4_update_org.py::test_update_org PASSED
test_5_delete_org.py::test_delete_org PASSED
```

---

#  **Test Suite Overview**

### `conftest.py`

* Overrides MongoDB with `mongomock`
* Ensures isolated TestClient for each test

### Tests included:

#### ✔ `test_1_create_org.py`

Validates organization creation

#### ✔ `test_2_login.py`

Tests admin authentication + JWT

#### ✔ `test_3_get_org.py`

Fetches organization metadata

#### ✔ `test_4_update_org.py`

Updates org info + verifies response

#### ✔ `test_5_delete_org.py`

Validates deletion permissions + cleanup

---

#  **High-Level Architecture Diagram**

```
                +-----------------------------+
                |        Master Database      |
                | organizations | admins      |
                +-----------------------------+
                           |
                           |
          +-----------------------------------------+
          |             Backend API (FastAPI)       |
          |-----------------------------------------|
          |  /org/create      /org/get              |
          |  /org/update      /org/delete           |
          |  /admin/login  --> JWT Auth             |
          +-----------------------------------------+
                           |
                           |
            +-------------------------------+
            |   Dynamic Org Databases       |
            |   org_companyA                |
            |   org_companyB                |
            +-------------------------------+
```

---

#  **Scalability Notes **

### ✔ Pros

* True multi-tenant isolation
* Easy horizontal scaling
* FastAPI provides excellent performance
* MongoDB dynamic schema fits varying org-level data

### ✔ Trade-Offs

* Too many collections → monitoring overhead
* Harder to run cross-organization analytics
* Migrating schemas requires iterating over all collections

### ✔ Possible Improvements

A more scalable enterprise design could use:

#### **1. Shared tables with `tenant_id`**

* Better indexing
* Single schema to manage
* Easy sharding

#### **2. Event-driven provisioning**

* Organization creation triggers async worker
* Improved API responsiveness

#### **3. RBAC (Role-Based Access Control)**

More secure admin/user structure per tenant.


---
