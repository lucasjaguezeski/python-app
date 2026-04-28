# Versão simplificada, somente com .whl
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY dist/*.whl .

RUN pip install --no-cache-dir *.whl \
    && rm *.whl

EXPOSE 8000

ENTRYPOINT ["python", "-m", "app"]
