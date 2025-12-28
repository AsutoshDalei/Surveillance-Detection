FROM python:3.10-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY streamlitView.py .
COPY feedConnection.py .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "streamlitView.py", "--server.port=8501", "--server.address=0.0.0.0"]

