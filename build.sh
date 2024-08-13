#!/bin/bash

# Docker 이미지 빌드
docker build -t ampersandor/dna-visualizer .

# DockerHub에 푸시
docker push ampersandor/dna-visualizer

