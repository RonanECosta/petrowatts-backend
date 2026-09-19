FROM python:3.11-slim

WORKDIR /app

# Instala dependências essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da sua aplicação para o container
COPY . .

# Expõe a porta padrão do Flask
EXPOSE 5000

# Como você está usando flask-openapi3, o comando para rodar deve escutar em '0.0.0.0'
# (Se no final do seu app.py já tiver if __name__ == '__main__': app.run(host='0.0.0.0'), 
# você pode usar apenas ["python", "app.py"]). Caso contrário, use o comando abaixo:
CMD ["python", "app.py"]