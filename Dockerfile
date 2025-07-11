FROM python:3.10-slim-bullseye

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    exiftool \
    steghide \
    binwalk \
    imagemagick-6.q16 \
    ruby \
    ruby-dev \
    build-essential \
    chromium \
    chromium-driver \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN gem install zsteg

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x src/steganography/*.sh

ENTRYPOINT ["python3", "src/main.py"]

CMD ["--help"]
