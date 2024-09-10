
FROM python:3.9-slim

WORKDIR /app # setting working directory in the container
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt     #to install any needed packages specified in requirements.txt
EXPOSE 80
ENV NAME EthereumDepositTracker         #environment variable

CMD ["python", "ethereum_deposit_tracker.py"]   #runs the app whenever the container is launched. 
