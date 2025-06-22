# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "support_ticket.py", "--server.port=8501", "--server.address=0.0.0.0"]
