include dispatch-engine/.env

start_workers:
	cd dispatch-engine && python -m app.apis.dispatch.start_workers

start_tasks:
	cd dispatch-engine && python -m app.apis.dispatch.start_tasks

start_monitor:
	rq-dashboard -u redis://$(DEV_REDIS_
docker_up:
	docker-compose -f "dispatch-engine/docker-compose.yml" up -d redis
