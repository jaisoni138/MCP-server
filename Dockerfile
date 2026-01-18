FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv pip install --system fastmcp mcpo

RUN pip install pandas openpyxl

# Expose the port the proxy server will run on
EXPOSE 8000

# The command is defined in docker-compose.yml for each service
CMD ["true"]
