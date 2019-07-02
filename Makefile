DOCKERFILE := Dockerfile

PYTHON := python

CONTAINER_NAME := gh_wrapper

PROD_IMAGE := gh_wrapper:alpine_prod
DEV_IMAGE := gh_wrapper:alpine_dev
IMAGE := $(PROD_IMAGE)
SAVE_IMAGE_FILE := gh_wrapper_local_image_alpine_prod.tar.gz
# BUILD_ARGS := --build-arg TZ=Asia/Yekaterinburg --build-arg DEVEL="false" --build-arg APP_PATH=/opt/gtfs_getter
BUILD_ARGS :=

build:
	docker build -f $(DOCKERFILE) -t $(IMAGE) $(BUILD_ARGS) .

save:
	docker save $(IMAGE) | gzip > $(SAVE_IMAGE_FILE)

APP_DIR := $(shell pwd)

all: build save


build_alpine_prod:
	# make build DOCKERFILE=$(DOCKERFILE) IMAGE=$(PROD_IMAGE)
	make build IMAGE=$(PROD_IMAGE)

build_alpine_devel:
	make build IMAGE=$(DEV_IMAGE) BUILD_ARGS='--build-arg DEVEL="true"'


CMD := gunicorn -c config.py wsgi
run:
	docker run --rm --name=$(CONTAINER_NAME) $(DOCKER_ARGS) -it $(IMAGE) $(CMD) $(ARGS)

run_advanced:
	@echo UID is $(shell id -u)
	@echo GID is $(shell id -g)
	make run IMAGE=$(IMAGE) DOCKER_ARGS="-p 9990:9990 \
		--memory-swappiness=0 \
        --cap-add=SYS_PTRACE  \
        --memory=2G \
		--net=host \
		--name=$(CONTAINER_NAME) \
		-e HOME=/root \
		-v $(shell pwd)/:/opt/graphhopper_wrapper/  \
		-v $(shell pwd)/.docker_root_home:/root/  "

postbuild_dev:
	# обновляет смапленные (-v) директории
	make run_dev CMD='$(PYTHON) setup.py develop'

all: build run


