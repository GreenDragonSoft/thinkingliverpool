ASSETS = thinkingweekly/assets
STATIC = thinkingweekly/static

SASS_FILES = $(ASSETS)/stylesheets/app.scss $(ASSETS)/stylesheets/app/thinkingliverpool.scss

all: $(STATIC)/css/combined.min.css $(STATIC)/js/combined.min.js

$(STATIC)/css/combined.min.css: $(SASS_FILES)
	sass $(ASSETS)/stylesheets/app.scss $@ --style compressed

$(STATIC)/js/combined.min.js: $(ASSETS)/js/jquery-3.1.1.min.js $(ASSETS)/js/bootstrap.min.js
	cat $^ > $@

.PHONY: clean
clean:
	rm -f $(STATIC)/css/combined.min.css
	rm -f $(STATIC)/css/combined.min.js


.PHONY: test
test:
	./manage.py test -v 3 --failfast

.PHONY: runserver
runserver:
	./manage.py runserver 0.0.0.0:8000

.PHONY: dumpdb
dumpdb: latest.sql
       echo 'Now do vagrant ssh, then: dropdb vagrant && createdb vagrant && psql < latest.sql'

latest.dump:
	heroku pg:backups capture --app thinkingweekly
	curl -o latest.dump `heroku pg:backups public-url`

latest.sql: latest.dump
	# convert dump file to SQL
	pg_restore --no-acl --no-owner -f latest.sql latest.dump



.PHONY: tunnel
tunnel:
	ngrok http -region=eu -subdomain=thinkingweekly-xegef 8000
