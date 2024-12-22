# Utilizar imagem mínima com Python 3.12
FROM python:3.12.7-alpine

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apk add --no-cache gcc musl-dev libpq

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta em que o Gunicorn vai rodar
EXPOSE 8000

# Rodar o Gunicorn para servir a aplicação Django
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "BarberEasy.wsgi:application"]
