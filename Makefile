.PHONY: test
test:
	./manage.py test -v 3 --failfast

.PHONY: runserver
runserver:
	./manage.py runserver 0.0.0.0:8000

.PHONY: backup
backup:
	pg_dumpall > "backup_$(shell date --rfc-3339=seconds).sql"

.PHONY: tunnel
tunnel:
	ngrok http -region=eu -subdomain=thinkingweekly-xegef 8000
