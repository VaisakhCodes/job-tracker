version: "3.9"

services:
  db:
    image: postgres:16
    container_name: jobtracker_db
    environment:
      POSTGRES_USER: tracker_user
      POSTGRES_PASSWORD: tracker_pass
      POSTGRES_DB: jobtracker
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data: 