# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/app

# Install git (sometimes needed for dbt packages, good practice)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy your requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your dbt project into the container
COPY . .

# Set the default command to run your dbt pipeline (seed, run, test)
CMD ["sh", "-c", "dbt seed --profiles-dir . && dbt run --profiles-dir . && dbt test --profiles-dir ."]
