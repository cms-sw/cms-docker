.PHONY: all build

BUILD_REPO := gartung/dxr
TAG ?= $(shell date +%F_%H-%M)

all: build
	@echo "done"

build: Dockerfile
	docker build  --tag=$(BUILD_REPO):$(TAG) .
	docker tag --force $(BUILD_REPO):$(TAG) $(BUILD_REPO):latest

upload: build
	docker push $(BUILD_REPO):$(TAG)

