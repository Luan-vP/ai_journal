#!/bin/bash

docker tag ai_journal-backend gcr.io/alabaster-therapy-demo/ai_journal-backend
docker push gcr.io/alabaster-therapy-demo/ai_journal-backend

docker tag ai_journal-frontend gcr.io/alabaster-therapy-demo/ai_journal-frontend
docker push gcr.io/alabaster-therapy-demo/ai_journal-frontend

# # Get the list of docker images
# docker images --format "{{.Repository}}:{{.Tag}}" | while read -r image; do
#   echo "Uploading $image"
#   docker push "$image"
# done