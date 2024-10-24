# Use the official Python 3.7 image from Docker Hub
FROM python:3.7-slim

# Set the working directory inside the container
WORKDIR /usr/local/app

# Install Jupyter and application dependencies
RUN pip install --no-cache-dir jupyter
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY /src/ ./src/

# Command to run Jupyter notebook in the container
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
