# Step 1 — get Python
FROM python:3.11-slim

# Step 2 — set working directory inside container
WORKDIR /app

# Step 3 — copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4 — copy all your project files
COPY . .

# Step 5 — run the app
CMD ["sh", "-c", "uvicorn Fastapi:app --host 0.0.0.0 --port ${PORT:-10000}"]