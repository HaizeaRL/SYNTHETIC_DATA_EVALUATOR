# Use the official Python 3.7 image from Docker Hub
FROM python:3.7

# Set the working directory inside the container
WORKDIR /usr/local/app

# Install Jupyter
RUN pip install --no-cache-dir jupyter

# Install the application dependencies
COPY requirements.txt /src/sdv_synthetic_data.ipynb /src/synthetic_data_evaluation_and_comparation.ipynb ./
RUN pip install --no-cache-dir -r requirements.txt

# Command to run Jupyter notebook in the container
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
