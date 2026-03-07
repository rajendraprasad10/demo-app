# Approach:
# 1. Use lightweight python base image
# 2. Copy requirements
# 3. Install dependencies
# 4. Copy app
# 5. Run uvicorn

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6️⃣ Hardcoded environment secrets (Trivy secret scan will detect)
ENV AWS_ACCESS_KEY_ID="AKIAFAKEKEY123"
ENV AWS_SECRET_ACCESS_KEY="fakeSecretKey123456789"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

