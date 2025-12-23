# Jagdish koyeb + Render 

FROM python:3.10-slim

# Set working directory
WORKDIR /VJ-FILTER-BOT

# System packages
RUN apt update && apt install -y git \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better cache)
COPY requirements.txt .

# Upgrade pip & install python deps
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Start bot
CMD ["python3", "bot.py"]
