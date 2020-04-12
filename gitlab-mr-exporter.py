# Standard imports
from prometheus_client import start_http_server, Metric, REGISTRY
import time
import os
import gitlab
import multiprocessing
import urllib3
from functools import partial
from datetime import datetime, timezone

urllib3.disable_warnings()


def get_project(gl, project):
    project_info = {}
    project = gl.projects.get(project)
    project_info['project'] = project
    merge_requests = project.mergerequests.list(state='opened')
    project_info['merge_requests'] = merge_requests
    return project_info


def multiprocess_get_project(projects):
    gl = gitlab.Gitlab('https://gitlab.gitlab.maker.studio/', private_token='p-ovud1APuHTVGKgsVS8', ssl_verify=False)
    process_pool = multiprocessing.Pool(multiprocessing.cpu_count())
    partial_function = partial(get_project, gl)
    data = process_pool.map(partial_function, projects)
    process_pool.close()
    return data


def return_days(merge_request):
    merge_request_date = merge_request.created_at
    merge_request_datetime = datetime.strptime(merge_request_date, '%Y-%m-%dT%H:%M:%S.%f%z')
    now = datetime.now(timezone.utc)  
    time_delta = now - merge_request_datetime
    time_delta_days = int(time_delta.seconds / 60 / 60 / 24)
    return time_delta_days


class GitlabCollector(object):
    def __init__(self):
        self._endpoint = '6666'

    def collect(self):
        gitlab_projects = os.getenv('GITLAB_PROJECTS').split(',')
        gitlab_url = os.getenv('GITLAB_URL')
        gitlab_token = os.getenv('GITLAB_TOKEN')

        projects_data = multiprocess_get_project(gitlab_projects)

        gitlab_mr = Metric(
            'gitlab_mr', 'Metric to represent a Gitlab Merge request', 'gauge')

        for project in projects_data:
            for merge_request in project['merge_requests']:
                gitlab_mr.add_sample('gitlab_mr', value=return_days(merge_request), labels={
                'project_name': project['project'].name,
                'mr_title': merge_request.title,
                'upvotes': str(merge_request.upvotes),
                'downvotes': str(merge_request.downvotes),
                'author': merge_request.author['name'],
                'url': merge_request.web_url,
                'has_conflicts': str(merge_request.has_conflicts),
                'work_in_progress': str(merge_request.work_in_progress),
                'source_branch': str(merge_request.source_branch),
                'target_branch': str(merge_request.target_branch)
                })

        yield gitlab_mr


if __name__ == '__main__':
    start_http_server(6666)
    REGISTRY.register(GitlabCollector())
    while True:
        time.sleep(30)
