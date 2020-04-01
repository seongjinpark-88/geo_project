# This Dockerfile has two required ARGs to determine which base image
# to use for the JDK and which sbt version to install.

ARG OPENJDK_TAG=8u212
FROM openjdk:${OPENJDK_TAG}
# FROM ubuntu:16.04
MAINTAINER Seongjin Park

ARG SBT_VERSION=1.2.8
ENV HOME=/home/seongjinpark/research/git_repo/geo_project

RUN apt-get update -qq\
 && apt-get install --no-install-recommends -y \
  graphviz \
  git \
  gcc \
  python \
  python3 \
  python-setuptools \
  python-numpy \
  python-dev \
  python-pip \
  libssl-dev \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  libevent-dev \
  python3-setuptools \
  python3-numpy \
  python3-dev \
  python3-pip \
  build-essential \
  tmux \
  unzip \
  curl \
  zlib1g-dev \
  make \
  wget \
  curl \
  patch \
  bzip2 \
 && apt-get clean

# Install sbt
RUN \
 curl -L -o sbt-$SBT_VERSION.deb https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb && \
  dpkg -i sbt-$SBT_VERSION.deb && \
  rm sbt-$SBT_VERSION.deb && \
  apt-get update && \
  apt-get install sbt && \
  sbt sbtVersion

# RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
# RUN curl -sL "https://keyserver.ubuntu.com/pkslookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
# RUN apt-get update
# RUN apt-get install sbt
# RUN sbt sbtVersion


RUN pip3 install --upgrade pip
RUN pip3 install -U spacy
RUN pip3 install scikit-learn numpy joblib matplotlib geopy folium certifi


WORKDIR ${HOME}

