# Use the official Python 3.7 image from Docker Hub
FROM python:3.7-slim

# Set the working directory inside the container
WORKDIR /usr/local/app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Download and install RAR (required for creating .rar files)
RUN curl -O https://www.rarlab.com/rar/rarlinux-x64-701.tar.gz && \
    tar -zxvf rarlinux-x64-701.tar.gz && \
    rm rarlinux-x64-701.tar.gz && \
    cd rar && \
    install -c rar unrar /usr/local/bin/ && \
    cd .. && rm -rf rar

# Install Jupyter and application dependencies
RUN pip install --no-cache-dir jupyter
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY /src/ ./src/
COPY /resources/ ./resources/
COPY /results/ ./results/

# Command to run Jupyter notebook in the container
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
