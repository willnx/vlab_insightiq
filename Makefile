clean:
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info
	-rm -f tests/.coverage
	-docker rm `docker ps -a -q`
	-docker rmi `docker images -q --filter "dangling=true"`

build: clean
	python setup.py bdist_wheel --universal

uninstall:
	-pip uninstall -y vlab-insightiq-api

install: uninstall build
	pip install -U dist/*.whl

test: uninstall install
	cd tests && nosetests -v --with-coverage --cover-package=vlab_insightiq_api

images: build
	sudo docker build -f ApiDockerfile -t willnx/vlab-insightiq-api .
	sudo docker build -f WorkerDockerfile -t willnx/vlab-insightiq-worker .

up:
	docker-compose -p vlabinsightiq up --abort-on-container-exit
