### How to build
```
make docker-build-and-push
```

### Required ENV variables
```
export GITLAB_TOKEN=$TOKEN_HERE
export GITLAB_URL=https://$GITLAB_URL_HERE
# Comma separated gitlab ID of projects that need to be monitored
# export GITLAB_PROJECTS=1,2,3,4,5
export GITLAB_PROJECTS=$
```
