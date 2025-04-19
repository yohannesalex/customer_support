FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
# Copy application code and entrypoint
COPY . .
COPY requirements.txt .

COPY pyproject.toml poetry.lock* ./

# Accept DATABASE_URL as a build argument
ARG DATABASE_URL
# Set it as an environment variable inside the container
ENV DATABASE_URL=${DATABASE_URL}


RUN chmod +x entrypoint.sh

# Install dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install 

RUN cat requirements.txt | xargs poetry add

RUN useradd -m appuser
USER appuser
    
    
EXPOSE 9000

# Use an entrypoint that first runs Alembic migrations then starts the API
CMD ["./entrypoint.sh"]


