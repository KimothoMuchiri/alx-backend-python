# use the base python image
FROM python:3.10

# System packages:
RUN apt-get update && apt-get install -y --no-install-recommends \
      default-mysql-client \
      default-libmysqlclient-dev \
      build-essential \
      pkg-config \
    && rm -rf /var/lib/apt/lists/*

# set the workind dir to inside the container
WORKDIR /usr/src/app

# Install the dependencies
COPY requirements.txt ./

# Install packages using the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your app code into the container
COPY . .

# 4. Expose the port your Django app runs on (default is 8000)
EXPOSE 8000

# 5. Define the command to run the application when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]