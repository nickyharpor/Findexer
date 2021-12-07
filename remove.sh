#!/bin/bash

docker stop kibana es01 es02 es03 findexer
docker rm kibana es01 es02 es03 findexer
docker rmi findexer
rm -rf data*

