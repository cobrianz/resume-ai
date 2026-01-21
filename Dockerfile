FROM python:3.10-slim

WORKDIR /code

# Copy requirements first (for better caching)
COPY ./requirements.txt /code/requirements.txt

# Install dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade wheel && \
    pip install --no-cache-dir -r /code/requirements.txt

# Copy app code
COPY ./app /code/app

# Copy frontend
COPY ./frontend /code/frontend

# Set environment variables
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
