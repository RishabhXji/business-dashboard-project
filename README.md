# Retail Sales & Inventory Analytics Dashboard

Project: Retail Sales & Inventory Analytics Dashboard

Overview
--------
A full-stack Business Intelligence dashboard that processes retail sales data and exposes analytics, KPIs, visualizations, and business insights. Built with React (Vite) frontend and FastAPI backend, it is designed to be modular, scalable, and resume-worthy.

Architecture
------------
- Frontend: React + Vite + Tailwind CSS + Recharts
- Backend: FastAPI, pandas, SQLAlchemy-compatible structure
- Data: CSV / PostgreSQL-compatible design (includes a data generator for 50k rows)

Getting started (backend)
-------------------------
1. Create a Python virtualenv and activate it
   python -m venv venv
   .\\venv\\Scripts\\activate

2. Install dependencies
   pip install -r backend/requirements.txt

3. Generate dataset (creates database/sales_data.csv)
   python backend\\app\\data\\generate_data.py

4. Run the API
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API Endpoints
-------------
- GET /dashboard
- GET /sales
- GET /products
- GET /customers
- GET /inventory
- GET /forecast
- GET /insights

Frontend
--------
A minimal frontend scaffold is provided in frontend/. Extend it with React, Tailwind, and charts to build the full UI.

Future Improvements
-------------------
- Complete React frontend with authentication, charts, filters, dark mode
- Persist dataset to PostgreSQL and use SQLAlchemy models + Alembic migrations
- Add export to PDF / Excel features
- Add real forecasting models (ARIMA / Prophet)
- Add tests, CI, and Docker deployment

This project demonstrates retail analytics, KPI calculations, data-processing with Python/pandas, REST API design with FastAPI, and a modern React dashboard front-end.
