FROM python:3.13-slim-bookworm

# Copy application code
COPY app ./app
COPY requirements.txt .
COPY img1.bmp ./img1.bmp
COPY img2.bmp ./img2.bmp

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8012

CMD [\
    "uvicorn", \
    "app.main:app", \
    "--host", \
    "0.0.0.0", \
    "--port", \
    "8012"\
    ]