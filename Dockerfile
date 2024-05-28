# Use a specific version of the Python slim-buster image
FROM python:3.11.4-slim-buster

ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
# Set working directory
WORKDIR $APP_HOME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
# Устанавливаем зависимости, описанные в файле requirements.txt
RUN pip install -r requirements.txt

# Copy entrypoint script and set permissions
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project
COPY . $APP_HOME

# Specify the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
