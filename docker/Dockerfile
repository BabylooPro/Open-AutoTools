########################################################
#                   UBUNTU STAGE                       #
########################################################

ARG PYTHON_VERSION=3.12

FROM ubuntu:24.04 AS builder
ARG PYTHON_VERSION

# PREVENT INTERACTIVE PROMPTS DURING BUILD
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# SET WORKING DIRECTORY
WORKDIR /app

# CREATE AND ACTIVATE VIRTUAL ENVIRONMENT
ENV VIRTUAL_ENV=/opt/venv
RUN python${PYTHON_VERSION} -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# UPGRADE PIP AND INSTALL BUILD DEPENDENCIES
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# COPY PROJECT FILES
COPY . .

# INSTALL PROJECT IN EDITABLE MODE
RUN pip install --no-cache-dir -e .

# UBUNTU STAGE
FROM ubuntu:24.04 AS ubuntu
ARG PYTHON_VERSION

# PREVENT INTERACTIVE PROMPTS DURING BUILD
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL RUNTIME DEPENDENCIES
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    ffmpeg \
    xclip \
    xsel \
    openjdk-17-jre-headless \
    bc \
    && rm -rf /var/lib/apt/lists/*

# COPY VIRTUAL ENV FROM BUILDER
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# SET WORKING DIRECTORY
WORKDIR /app

# COPY PROJECT FILES FROM BUILDER
COPY --from=builder /app /app

# SET ENTRYPOINT TO TEST SCRIPT
ENTRYPOINT ["bash", "/app/docker/run_tests.sh"]


########################################################
#        SLIM STAGE (USED FOR macos/windows)           #
########################################################

FROM python:${PYTHON_VERSION}-slim AS slim-builder
ARG PYTHON_VERSION

# INSTALL BUILD DEPENDENCIES (KEEP RUNTIME IMAGE SMALL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# SET WORKING DIRECTORY
WORKDIR /app

# CREATE AND ACTIVATE VIRTUAL ENVIRONMENT
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# UPGRADE PIP AND INSTALL BUILD DEPENDENCIES
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# COPY PROJECT FILES
COPY . .

# INSTALL PROJECT IN EDITABLE MODE
RUN pip install --no-cache-dir -e .

FROM python:${PYTHON_VERSION}-slim AS slim
ARG PYTHON_VERSION

# INSTALL RUNTIME DEPENDENCIES
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    default-jre-headless \
    bc \
    && rm -rf /var/lib/apt/lists/*

# COPY VIRTUAL ENV FROM BUILDER
ENV VIRTUAL_ENV=/opt/venv
COPY --from=slim-builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# SET WORKING DIRECTORY
WORKDIR /app

# COPY PROJECT FILES FROM BUILDER (ALLOWS RUNNING WITHOUT BIND-MOUNT)
COPY --from=slim-builder /app /app

# SET ENTRYPOINT TO TEST SCRIPT
ENTRYPOINT ["bash", "/app/docker/run_tests.sh"]

FROM slim AS macos
FROM slim AS windows
