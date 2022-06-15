#!/bin/bash

docker build . --tag featurecloud.ai/federated_svd
docker push featurecloud.ai/federated_svd
