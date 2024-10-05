# ### Build and install packages
# FROM python:3.11-slim as python-base

# # Add user that will be used in the container.
# RUN useradd student

# # Port used by this container to serve HTTP.
# EXPOSE 8000

# # Install Python dependencies
# ENV PYTHONUNBUFFERED=1 \
#     # prevents python creating .pyc files
#     PYTHONDONTWRITEBYTECODE=1 \
#     \
#     # pip
#     PIP_NO_CACHE_DIR=off \
#     PIP_DISABLE_PIP_VERSION_CHECK=on \
#     PIP_DEFAULT_TIMEOUT=100 \
#     \
#     PYSETUP_PATH="/opt/pysetup" \
#     VENV_PATH="/opt/pysetup/.venv"

# # prepend poetry and venv to path
# ENV PATH="$VENV_PATH/bin:$PATH"

# # Install system packages required by Wagtail and Django.
# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libwebp-dev \
#     netcat-traditional \
#     tree \
#  && rm -rf /var/lib/apt/lists/*

# # Set the working directory to /tmp.
# # WORKDIR /tmp

# # Install the application server.
# RUN pip install "gunicorn==20.0.4"

# # Upgrade pip.
# RUN pip install --upgrade pip

# # Use /app folder as a directory where the source code is stored.
# WORKDIR /app

# # Set this directory to be owned by the "blogger" user. This Wagtail project
# # uses SQLite, the folder needs to be owned by the user that
# # will be writing to the database file.
# RUN chown student:student /app

# # Copy the source code of the project into the container.
# COPY --chown=student:student . .



# RUN pip install -r ./requirements.txt

# # Collect static files.
# # RUN python manage.py collectstatic --noinput --clear

# # Runtime command that executes when "docker run" is called, it does the
# # following:
# #   1. Migrate the database.
# #   2. Start the application server.
# # WARNING:
# #   Migrating database at the same time as starting the server IS NOT THE BEST
# #   PRACTICE. The database should be migrated manually or using the release
# #   phase facilities of your hosting platform. This is used only so the
# #   Wagtail instance can be started with a simple "docker run" command.
# # CMD set -xe; python manage.py migrate --noinput
# #CMD gunicorn config.wsgi:application
# # CMD daphne -b $HOST_URL -p $HOST_PORT server.asgi:application
# #CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "server.asgi.gunicorn_worker.UvicornWorker", "server.asgi:application"]
# # gunicorn --bind 0.0.0.0:8000 jwt_berry.asgi -w 4 -k uvicorn.workers.UvicornWorker

# # copy docker-entrypoint.sh
# COPY  --chown=student:atudent ./docker-entrypoint.sh ./docker-entrypoint.sh

# RUN chmod +x docker-entrypoint.sh

# USER blogger

# ENTRYPOINT ["./docker-entrypoint.sh"]





FROM python:3.11-slim as python-base

# Add user that will be used in the container.
RUN useradd student

# Port used by this container to serve HTTP.
EXPOSE 8000

# Install Python dependencies
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Prepend poetry and venv to path
ENV PATH="$VENV_PATH/bin:$PATH"

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat-openbsd \ 
    tree \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Upgrade pip.
RUN pip install --upgrade pip

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "student" user.
RUN chown student:student /app

# Copy the source code of the project into the container.
COPY --chown=student:student . .

# Install Python dependencies
RUN pip install -r ./requirements.txt

# Copy docker-entrypoint.sh
COPY --chown=student:student ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

USER student

ENTRYPOINT ["./docker-entrypoint.sh"]
