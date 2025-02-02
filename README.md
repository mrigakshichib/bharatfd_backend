Here is a **detailed and well-structured `README.md`** for your **Django multilingual FAQ system** with caching, WYSIWYG support, and testing.  

---

# **  Django Multilingual FAQ System with Caching & WYSIWYG Editor**

## **  Overview**
This project is a **Django-based FAQ system** that supports:
-   **Multilingual FAQs** with automatic translation (Google Translate API)
-   **WYSIWYG Editor (`django-ckeditor`)** for rich text content
-   **Caching with Redis (`django-redis`)** for faster translations
-   **REST APIs (`Django REST Framework`)** for easy frontend integration
-   **Unit Testing (`pytest`)** for robust validation

---

## **  Installation & Setup**
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/mrigakshichib/bharatfd_backend.git
cd multilingual_faq
```

### **  Step 2: Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### **  Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **  Step 4: Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **  Step 5: Start Redis Server**
Make sure Redis is running:
```bash
redis-server
```
You can verify Redis is working by running:
```bash
redis-cli ping
# Response should be: PONG
```

### **  Step 6: Create Super User**

```bash
python manage.py createsuperuser
```
you can setup your own username and password then!

### **  Step 7: Start Django Development Server**
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/admin/`** to access the Django Admin Panel.

---

## **  2️⃣ Features**
###   **Multilingual FAQ System**
- Users can store questions and answers in **English**.
- Translations for **Hindi (`hi`), Bengali (`bn`) are stored in **Redis Cache**.

###   **WYSIWYG Editor (`django-ckeditor`)**
- Rich text support for FAQ answers.
- Bold, italic, images, lists, links, and more formatting.

###   **Caching with Redis**
- **Translations are cached** to prevent unnecessary API calls.
- **FAQs are stored in memory** for faster access.

###   **REST API (`Django REST Framework`)**
- Provides **POST and GET operations** for managing FAQs.

---

## **  3️⃣ API Endpoints**
| Method | Endpoint | Description |
|--------|---------|------------|
| **GET** | `/api/faqs/` | Fetch all FAQs (default in English) |
| **GET** | `/api/faqs/?lang=hi` | Fetch FAQs in **Hindi** |
| **POST** | `/api/faqs/` | Create a new FAQ |


### **  Example API Requests**
####   **1. Get FAQs in English (Default)**
```bash
curl -X GET "http://127.0.0.1:8000/api/faqs/"
```

####   **2. Get FAQs in Hindi**
```bash
curl -X GET "http://127.0.0.1:8000/api/faqs/?lang=hi"
```

####   **3. Get FAQs in Bengali**
```bash
curl -X GET "http://127.0.0.1:8000/api/faqs/?lang=bn"
```

####   **4. Create a New FAQ**
```bash
curl -X POST "http://127.0.0.1:8000/api/faqs/" \
-H "Content-Type: application/json" \
-d '{
    "question": "What is Django?",
    "answer": "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design."
}'
```

---

## **  4️⃣ How Caching Works**
1. **When a new FAQ is created:**
   - Translations for **Hindi (`hi`), Bengali (`bn`)** are stored in **Redis Cache**.
   - The original **English question & answer are stored in the database**.

2. **On every API request:**
   - If translations **exist in Redis**, they are served directly (**cache hit**).
   - If translations **do not exist**, they are fetched via Google Translate API and **stored in Redis**.

3. **Cache Invalidation:**
   - When an FAQ is **updated** or **deleted**, old cached translations are **removed** to ensure fresh data.

---

## **  5️⃣ Running Tests**
### **  Step 1: Install Testing Dependencies**
```bash
pip install pytest pytest-django
```

### **  Step 2: Run All Tests**
```bash
pytest -v
```

### **  Step 3: Run Specific Test**
Run only the FAQ API tests:
```bash
pytest faqs/tests/test_views.py
```

---

**Run `python manage.py runserver` and start using it today!** 