start_worker:
	cd dispatch-engine && python -m app.apis.dispatch.start_worker


start_task:
	cd dispatch-engine && python -m app.apis.dispatch.start_task

start_monitor:
	rq-dashboard
