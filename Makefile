start_workers:
	cd dispatch-engine && python -m app.apis.dispatch.start_workers


start_tasks:
	cd dispatch-engine && python -m app.apis.dispatch.start_tasks

start_monitor:
	rq-dashboard
