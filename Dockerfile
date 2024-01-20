#Deriving the latest base image
FROM python:3.10.13

# Set the working directory in the container
WORKDIR /app

#copy the source code to app directory
COPY . /app

#install requirements
RUN pip install -r req.txt

# Expose the port that your application listens on
EXPOSE 8000

#cmd to run on container start
CMD [ "python", "./index.py" ]