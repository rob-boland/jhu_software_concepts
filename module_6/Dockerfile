# Pull python 3.10
FROM python:3.10

# Create /app directory and change to /app
RUN mkdir /app
WORKDIR /app

# Add main python file and flask structure for module
ADD run.py .
ADD boland_website ./boland_website

# Install all requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# App runs on port 8080 be default
EXPOSE 8080

# Run run.py
CMD ["python", "run.py"]