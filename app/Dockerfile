FROM python:3.13-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7

COPY . /app

WORKDIR /app

EXPOSE 4000

# Essa variável de ambiente é usada para controlar se o Python deve
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE=1

# Define que a saída do Python será exibida imediatamente no console ou em
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED=1

# RUN executa comandos em um shell dentro do container para construir a imagem.
# O resultado da execução do comando é armazenado no sistema de arquivos da
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da
# imagem e torná-la mais eficiente.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /app/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chmod -R 755 /data/web/static && \
  chmod -R +x ./start.sh

# Adiciona a pasta scripts e venv/bin
# no $PATH do container.
ENV PATH="/venv/bin:$PATH"

# Muda o usuário para duser
USER duser

ENTRYPOINT ["./start.sh"]
CMD ["runserver", "0.0.0.0:4000"]