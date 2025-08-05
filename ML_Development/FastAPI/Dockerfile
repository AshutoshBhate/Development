FROM python:3.12.4

WORKDIR /usr/src/app
# From this point onwards, all operations will happen inside /usr/src/app within the image

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#Copies files from the local system on to the Docker image
COPY . .            

CMD ["uvicorn", "app.main_Routers:app", "--host", "0.0.0.0", "--port", "8000"]

#Queries : (environ) C:\Users\ashut\Development\ML_Development\FastAPI>

## To build the Docker image locally from the Dockerfile in the current directory, and tag it with your Docker Hub username and repository name:
#docker build -t ashutoshbhate/fastapi:latest .
##It looks for Dockerfile for default. If we had a 'Dockerfile.ubuntu', then to run the ubuntu sleeper say, we would have to use the '-f' flag
#docker build -t ashutoshbhate/ubuntu-sleeper:latest -f Dockerfile.ubuntu .
#docker run ashutoshbhate/ubuntu-sleeper:latest


## To push the locally built image to Docker Hub:
# docker push ashutoshbhate/fastapi:latest

## To view all Docker images present on your local machine:
# docker image ls

## To view all running Docker containers:
# docker ps

## To view all Docker containers (running and stopped):
# docker ps -a

