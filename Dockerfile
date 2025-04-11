FROM python:3.11

# Working directory
WORKDIR /app

COPY ./resources ./resources

# Exponer el puerto del servidor de recursos
EXPOSE 8083

# Comando para iniciar el servidor HTTP en /app/resources
CMD ["python", "-m", "http.server", "8083"]
