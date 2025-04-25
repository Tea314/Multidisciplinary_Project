# Multidisciplinary_Project
A Multidisciplinary Project combines knowledge from different fields to solve problems efficiently. It fosters teamwork, creativity, and innovation by integrating diverse perspectives. Clear communication and collaboration are key to achieving practical solutions.



# Fault Detection Backend

This is a **Go-based backend** for a fault detection system, designed to **store and retrieve fault records** (e.g., cracks, scratches) detected in products. The system uses **MongoDB** for data storage and provides a **RESTful API** built with the **Gin** framework.

Planned feature: integration with a `/detect` endpoint that communicates with a **Python-based YOLO service** for AI-powered fault detection.

---

## 🚀 Recent Development Summary

- **Project Setup**: Modular Go project with the following structure:
  - `internal/config`: Configuration
  - `pkg/mongodb`: MongoDB client
  - `internal/model`: Fault models
  - `internal/repository`: Repository layer
  - `internal/service`: Business logic
  - `internal/handler`: API handlers

- **Implemented API Endpoints**:
  - `POST /api/v1/faults`: Create new fault record
  - `GET /api/v1/faults/:id`: Retrieve fault record by MongoDB ObjectID

- **MongoDB Integration**:
  - Uses official MongoDB Go driver
  - Loads environment configuration from `.env`

- **Debugging Fixes**:
  - Fixed compilation errors: unused imports, undefined functions, redeclared variables
  - Handled import name conflicts
  - Corrected `FindByID` to properly use MongoDB ObjectID

- **Utilities**:
  - `query_faults.go`: Script to list fault records and ObjectIDs for testing

- **API Testing**:
  - Endpoints tested via `curl` and REST Client extension in VS Code

---

## ✅ Prerequisites

- [Go](https://golang.org/doc/install): v1.18 or later
- [MongoDB](https://www.mongodb.com/try/download/community): Local or Docker
- [VS Code](https://code.visualstudio.com/): Recommended for development
- Docker (optional): To run MongoDB
- curl or [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client): For testing API endpoints

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd fault-detection-backend
```
### 2. Install Dependencies

```bash
go mod tidy
go get github.com/gin-gonic/gin
go get go.mongodb.org/mongo-driver/mongo
go get github.com/joho/godotenv
```

### 3. Set Up MongoDB

Option 1: Using Docker (Recommended)
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

Option 2: Local Installation
```bash
mongod
```

### 4. Configure .env
Create a .env file in the root directory:
```env
MONGODB_URI=mongodb://localhost:27017
DB_NAME=fault_detection
PORT=8080
```

### 5. Run the Application
```bash
go build ./cmd/api
go run ./cmd/api/main.go
```
Server will start at: http://localhost:8080


