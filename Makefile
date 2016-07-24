.PHONY: test
test:
	./manage.py test -v 3 --failfast

.PHONY: runserver
runserver:
	./manage.py runserver 0.0.0.0:8000

.PHONY: dumpdb
dumpdb: latest.sql
       @echo 'Now do vagrant ssh, then: dropdb vagrant && createdb vagrant && psql < latest.sql'

latest.dump:
	heroku pg:backups capture
	curl -o latest.dump `heroku pg:backups public-url`

latest.sql: latest.dump
	# convert dump file to SQL
	pg_restore --no-acl --no-owner -f latest.sql latest.dump



.PHONY: tunnel
tunnel:
	ngrok http -region=eu -subdomain=thinkingweekly-xegef 8000
