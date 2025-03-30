FROM python:3.12

# Install dependencies
RUN apt update && apt install -y \
    build-essential \
    curl \
    wget \
    ca-certificates \
    libglib2.0-dev \
    libstdc++6 \
    libc6

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "src/main.py"]
