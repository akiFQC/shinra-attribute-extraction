FROM nvidia/cuda:11.0-base-ubuntu20.04

# Install Python
ENV PYTHON_VERSION 3.9.5
ENV HOME /root
ENV PYTHON_ROOT /usr/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
ENV PYENV_ROOT $HOME/.pyenv

WORKDIR "/root"

RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Tokyo

RUN apt-get update  && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    make \
    cmake \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
 && $PYENV_ROOT/plugins/python-build/install.sh \
 && /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT \
 && rm -rf $PYENV_ROOT

COPY pyproject.toml poetry.lock ./

RUN python -m venv .venv &&\
    pip install poetry && \
    poetry run pip install -U pip &&\
    poetry config virtualenvs.in-project true
