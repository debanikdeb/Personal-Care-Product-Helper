# Personal-Care-Product-Helper

An end-to-end Proof of Concept (POC) that combines:

* 🧠 **LLM-powered chatbot** for personal care product assistance
* 🗄️ **PostgreSQL-backed data layer**
* 🕸️ **Web scraping pipeline** for product extraction from Myntra

---

## 📌 Project Overview

This project fulfills the following requirements:

### ✅ 1. Personal Care Chatbot

* Built using **FastAPI + LangChain (Groq LLM)**
* Capable of:

  * Providing information about available products
  * Answering general queries (e.g., benefits of grooming products)
* Uses **product data stored in PostgreSQL**
* Handles special queries:

  * If user asks about **offers, returns, refunds, exchanges**
  * → Redirects to human support with contact number
* Uses **session-based memory (UUID)** for short conversational context
* Includes **sample/dummy data** for full workflow testing

---

### ✅ 2. Web Scraping (Myntra)

* Scrapes product data from:
  https://www.myntra.com/personal-care?f=Categories%3ALipstick
* Covers up to **5 pages**
* Extracts:

  * Product Name
  * Brand
  * Price
  * Ratings (if available)
  * Product URL
  * Breadcrumbs (e.g., `Home/Personal Care/Lipstick`)
* Outputs structured data into a **CSV file**

---

## 🛠️ Tech Stack

* **Backend**: FastAPI
* **LLM**: Groq (via LangChain)
* **Database**: PostgreSQL (pgAdmin)
* **ORM**: SQLAlchemy (Async)
* **Scraping**: Requests / BeautifulSoup (or equivalent)
* **Data Format**: JSON + CSV

---

## 📁 Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/debanikdeb/Personal-Care-Product-Helper.git
cd personal-care-chatbot-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SUPPORT_CONTACT=+91-XXXXXXXXXX
```

---

### 5. Initialize Database

```bash
python -m app.scripts.init_db
```

---

### 6. Populate Sample Product Data

Use API or script:

```bash
POST /api/v1/products/populate-products
```

---

## 🚀 Running the Server

Run the FastAPI server on **port 8008**:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8008 --reload
```

---

## 📡 API Endpoints

### 🔹 Health Check

```
GET /
```

---

### 🔹 Chatbot

```
POST /api/v1/chat/chat
```

#### Request:

```json
{
  "query": "Suggest a lipstick for dry lips",
  "session_id": "optional"
}
```

#### Response:

```json
{
  "session_id": "generated-or-existing",
  "response": "..."
}
```

---

### 🔹 Populate Products

```
POST /api/v1/products/populate-products
```

---

## 🧠 Chatbot Logic

* Uses **prompt-driven reasoning**
* Injects product data from DB as context
* Handles:

  * Product recommendations
  * Benefits explanation
* Special handling:

  * Queries like *offers / returns / refunds*
  * → Redirects to human support

---

## 📊 Scraping Module

Located in:

```
/scraper/
```

To run scraping script:

```bash
python scraper/myntra_scraper.py
```

Output:

```
data/products.csv
```

---

## ⚠️ Notes & Limitations

* Chat memory is **in-memory (not persistent)**
* No authentication implemented (POC scope)
* LLM responses depend on prompt quality
* Scraper may break if Myntra DOM changes

---

## 🔮 Future Improvements

* Add **RAG (vector search)** for scalable retrieval
* Use **Redis** for session memory
* Implement **LangGraph for tool orchestration**
* Add **frontend UI**
* Deploy on **AWS with CI/CD**

---

## 👤 Author

**Debanik Deb**
GitHub: https://github.com/debanikdeb

---

# Personal-Care-Product-Helper

An end-to-end Proof of Concept (POC) that combines:

* 🧠 **LLM-powered chatbot** for personal care product assistance
* 🗄️ **PostgreSQL-backed data layer**
* 🕸️ **Web scraping pipeline** for product extraction from Myntra

---

## 📌 Project Overview

This project fulfills the following requirements:

### ✅ 1. Personal Care Chatbot

* Built using **FastAPI + LangChain (Groq LLM)**
* Capable of:

  * Providing information about available products
  * Answering general queries (e.g., benefits of grooming products)
* Uses **product data stored in PostgreSQL**
* Handles special queries:

  * If user asks about **offers, returns, refunds, exchanges**
  * → Redirects to human support with contact number
* Uses **session-based memory (UUID)** for short conversational context
* Includes **sample/dummy data** for full workflow testing

---

### ✅ 2. Web Scraping (Myntra)

* Scrapes product data from:
  https://www.myntra.com/personal-care?f=Categories%3ALipstick
* Covers up to **5 pages**
* Extracts:

  * Product Name
  * Brand
  * Price
  * Ratings (if available)
  * Product URL
  * Breadcrumbs (e.g., `Home/Personal Care/Lipstick`)
* Outputs structured data into a **CSV file**

---

## 🛠️ Tech Stack

* **Backend**: FastAPI
* **LLM**: Groq (via LangChain)
* **Database**: PostgreSQL (pgAdmin)
* **ORM**: SQLAlchemy (Async)
* **Scraping**: Requests / BeautifulSoup (or equivalent)
* **Data Format**: JSON + CSV

---

## 📁 Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/debanikdeb/Personal-Care-Product-Helper.git
cd personal-care-chatbot-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
ENV=environment
FRONTEND_URL=your_local_frontend_url
BACKEND_URL=your_local_backend_url
GROQ_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
LANGCHAIN_ENDPOINT=langchain_endpoint
LANGCHAIN_API_KEY=your_api_key
LANGCHAIN_PROJECT=project_name
LANGCHAIN_TRACING_V2=true/false
TEMP_PATH=dir_name
```

---

### 5. Initialize Database

```bash
python -m app.scripts.init_db
```

---

### 6. Populate Sample Product Data

Use API or script:

```bash
POST /api/v1/products/populate-products
```

---

## 🚀 Running the Server

Run the FastAPI server on **port 8008**:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8008 --reload
```

---

## 📡 API Endpoints

### 🔹 Health Check

```
GET /
```

---

### 🔹 Chatbot

```
POST /api/v1/chatbot/chat
```

#### Request:

```json
{
  "query": "Suggest a lipstick for dry lips",
  "session_id": "optional"
}
```

#### Response:

```json
{
  "session_id": "generated-or-existing",
  "response": "..."
}
```

---

### 🔹 Populate Products

```
POST /api/v1/products/populate-products
```

### 🔹 Scrape Product Details & Store in CSV

```
POST /api/v1/extractor/scrape
```
#### Request:

```json
{
  "url": "https://www.myntra.com/personal-care?f=Categories%3ALipstick",
  "category_name": "lipstick"
}
```

#### Response:

```json
{
  "status": "success",
  "products_count": "...",
  "csv_download_url": "/downloads/extracted_products.csv",
  "pages_scraped": 5
}
```
---

## 🧠 Chatbot Logic

* Uses **prompt-driven reasoning**
* Injects product data from DB as context
* Handles:

  * Product recommendations
  * Benefits explanation
* Special handling:

  * Queries like *offers / returns / refunds*
  * → Redirects to human support

---


## ⚠️ Notes & Limitations

* Chat memory is **in-memory (not persistent)**
* No authentication implemented (POC scope)
* LLM responses depend on prompt quality
* Scraper may break if Myntra DOM changes

---

## 🔮 Future Improvements

* Add **RAG (vector search)** for scalable retrieval
* Use **Redis** for session memory
* Implement **LangGraph for tool orchestration**
* Implement **S3** for persistent file upload
* Add accessible downloadable link for CSV
* Add **frontend UI**
* Deploy on **AWS with CI/CD**

---

## 👤 Author

**Debanik Deb**
GitHub: https://github.com/debanikdeb

---

## 📄 License

This project is licensed under the Apache License 2.0.

You are free to use, modify, and distribute this software in compliance with the license terms.

See the LICENSE file for details:  
http://www.apache.org/licenses/LICENSE-2.0
