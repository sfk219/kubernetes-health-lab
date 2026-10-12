FROM python:3.12-slim
WORKDIR /app
COPY app ./app
USER 65532:65532
EXPOSE 8080
CMD ["python","-m","app.server"]
