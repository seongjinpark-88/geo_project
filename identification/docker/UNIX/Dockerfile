# This Dockerfile has two required ARGs to determine which base image
# to use for the JDK and which sbt version to install.

ARG OPENJDK_TAG=8u212
FROM openjdk:${OPENJDK_TAG}
MAINTAINER Seongjin Park

ARG SBT_VERSION=1.2.8
ENV HOME=/Users/seongjinpark/research/CLU/research/geo_project/identification

# Install sbt
RUN \
  curl -L -o sbt-$SBT_VERSION.deb https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb && \
  dpkg -i sbt-$SBT_VERSION.deb && \
  rm sbt-$SBT_VERSION.deb && \
  apt-get update && \
  apt-get install sbt && \
  sbt sbtVersion

WORKDIR ${HOME}

