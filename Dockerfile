# Use a lightweight Python image
FROM python:3.12.5-slim

# Set working directory
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose the port FastAPI runs on
EXPOSE 80

# Run the app
CMD ["uvicorn", "underwriting_agent.main:app", "--host", "0.0.0.0", "--port", "80"]
