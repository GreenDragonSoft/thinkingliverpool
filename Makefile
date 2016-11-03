ASSETS = thinkingweekly/assets
STATIC = thinkingweekly/static

all: $(STATIC)/css/combined.min.css $(STATIC)/js/combined.min.js
	

$(STATIC)/css/combined.min.css: $(ASSETS)/css/bootstrap.min.css $(ASSETS)/css/thinkingliverpool.min.css
	cat $^ > $@

$(STATIC)/js/combined.min.js: $(ASSETS)/js/jquery-3.1.1.min.js $(ASSETS)/js/bootstrap.min.js
	cat $^ > $@

$(ASSETS)/css/thinkingliverpool.min.css: $(ASSETS)/css/thinkingliverpool.css
	yui-compressor $? > $@

.PHONY: clean
clean:
	rm -f $(ASSETS)/css/thinkingliverpool.min.css
	rm -f $(STATIC)/css/combined.min.css


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
	heroku pg:backups capture
	curl -o latest.dump `heroku pg:backups public-url`

latest.sql: latest.dump
	# convert dump file to SQL
	pg_restore --no-acl --no-owner -f latest.sql latest.dump



.PHONY: tunnel
tunnel:
	ngrok http -region=eu -subdomain=thinkingweekly-xegef 8000
