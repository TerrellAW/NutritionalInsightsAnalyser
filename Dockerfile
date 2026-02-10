# Stage 1: Build Stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
# Install dependencies into a local folder to copy later
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime Stage
FROM python:3.12-slim
WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy optimized lambda script and data
COPY lambda_function.py .
COPY res/data.csv ./res/data.csv

# Ensure the scripts in .local/bin are in the PATH
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "lambda_function.py"]
