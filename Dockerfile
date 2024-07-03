FROM python:3.9.18

# Set the working directory to /app
WORKDIR /app


# Install Python dependencies
COPY ./scripts /app/scripts
COPY requirements_lx.txt /app
COPY ./model /app/model
RUN python -V
RUN pip install --upgrade pip
RUN pip install -r requirements_lx.txt

# Copy the current directory contents into the container at /app
# COPY . /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# CMD [ "python","pip list" ]
CMD [ "python","scripts/testfile.py" ]