#!/bin/bash -e

image_name=duartcs/filecollect
image_tag=latest
full_image_name=${image_name}:${image_tag}

docker build .. -f ../Dockerfile --target file-collect-app -t ${full_image_name}
docker push ${full_image_name}

docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
echo ${full_image_name}

