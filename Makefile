docker-build-and-push:
	sudo docker build . -t laurentfdumont/gitlab-mr-exporter:latest && sudo docker push laurentfdumont/gitlab-mr-exporter:latest
