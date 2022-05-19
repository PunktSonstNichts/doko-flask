# pip freeze > requirements.txt # to create requirements.txt file

# Base python package
FROM python:3.8-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the files
COPY . .

# Executable commands
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]