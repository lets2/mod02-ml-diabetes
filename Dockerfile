
# Use um imagem python oficial como base
FROM python:3.13-slim

# Defin diretório de trabalho onde as próximas diretivas serão executadas
WORKDIR /app

# Copia o conteudo do diretório atual para dentro do container em /app
COPY . /app

# Instala as dependências especificadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Faz a porta 5000 dentro do container ficar disponivel pro exterior
EXPOSE 5000

# Executa a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
