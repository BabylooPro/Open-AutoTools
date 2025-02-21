########################################################
#                   UBUNTU STAGE                       #
########################################################

FROM ubuntu:24.04 AS builder

# PREVENT INTERACTIVE PROMPTS DURING BUILD
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    python3-setuptools \
    git \
    ffmpeg \
    build-essential \
    xclip \
    xsel \
    openjdk-17-jre \
    bc \
    && rm -rf /var/lib/apt/lists/*

# SET WORKING DIRECTORY
WORKDIR /app

# CREATE AND ACTIVATE VIRTUAL ENVIRONMENT
ENV VIRTUAL_ENV=/opt/venv
RUN python3.12 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# UPGRADE PIP AND INSTALL BUILD DEPENDENCIES
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy cython rich>=13.7.0

# PRE-INSTALL PROBLEMATIC DEPENDENCIES
RUN pip install --no-cache-dir \
    psutil \
    netifaces \
    spacy==3.7.2 --no-deps && \
    pip install --no-cache-dir spacy[all]==3.7.2

# DOWNLOAD SPACY MODEL
RUN python -m spacy download en_core_web_sm

# COPY PROJECT FILES
COPY . .

# INSTALL PROJECT IN EDITABLE MODE
RUN pip install -e .

# UBUNTU STAGE
FROM ubuntu:24.04 AS ubuntu

# PREVENT INTERACTIVE PROMPTS DURING BUILD
ENV DEBIAN_FRONTEND=noninteractive

# INSTALL RUNTIME DEPENDENCIES
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    ffmpeg \
    xclip \
    xsel \
    openjdk-17-jre \
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

# COPY AND MAKE TEST SCRIPT EXECUTABLE
COPY run_tests.sh /app/run_tests.sh
RUN chmod +x /app/run_tests.sh

# SET ENTRYPOINT TO TEST SCRIPT
ENTRYPOINT ["/app/run_tests.sh"]


########################################################
#                   MACOS STAGE                        #
########################################################

# MACOS STAGE (using slim python image as base)
FROM python:3.12-slim AS macos

# INSTALL SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    ffmpeg \
    default-jre \
    git \
    build-essential \
    python3-dev \
    bc \
    && rm -rf /var/lib/apt/lists/*

# SET WORKING DIRECTORY
WORKDIR /app

# CREATE AND ACTIVATE VIRTUAL ENVIRONMENT
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# UPGRADE PIP AND INSTALL BUILD DEPENDENCIES
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy cython rich>=13.7.0

# PRE-INSTALL PROBLEMATIC DEPENDENCIES
RUN pip install --no-cache-dir \
    psutil \
    netifaces \
    spacy[all]==3.7.2

# DOWNLOAD SPACY MODEL
RUN python -m spacy download en_core_web_sm

# COPY PROJECT FILES
COPY . .

# INSTALL PROJECT IN EDITABLE MODE
RUN pip install -e .

# COPY AND MAKE TEST SCRIPT EXECUTABLE
COPY run_tests.sh /app/run_tests.sh
RUN chmod +x /app/run_tests.sh

# SET ENTRYPOINT TO TEST SCRIPT
ENTRYPOINT ["/app/run_tests.sh"]


########################################################
#                   WINDOWS STAGE                      #
########################################################

FROM python:3.11-slim AS windows

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build essentials and runtime dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    default-jre \
    bc \
    && rm -rf /var/lib/apt/lists/*

# SET WORKING DIRECTORY
WORKDIR /app

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# INSTALL BUILD DEPENDENCIES
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy cython rich>=13.7.0

# PRE-INSTALL PROBLEMATIC DEPENDENCIES
RUN pip install --no-cache-dir \
    psutil \
    netifaces \
    spacy[all]==3.7.2

# DOWNLOAD SPACY MODEL
RUN python -m spacy download en_core_web_sm

# COPY PROJECT FILES
COPY . .

# INSTALL PROJECT IN EDITABLE MODE
RUN pip install -e .

# COPY TEST SCRIPT
COPY run_tests.sh /app/run_tests.sh
RUN chmod +x /app/run_tests.sh

# SET ENTRYPOINT TO TEST SCRIPT
ENTRYPOINT ["bash", "/app/run_tests.sh"] 
