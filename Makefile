ASSETS = thinkingweekly/assets
STATIC = thinkingweekly/static

SASS_FILES = $(ASSETS)/stylesheets/app.scss $(ASSETS)/stylesheets/app/thinkingliverpool.scss

all: $(STATIC)/css/combined.min.css $(STATIC)/js/combined.min.js bootstrap_static_fonts

$(STATIC)/css/combined.min.css: $(SASS_FILES)
	sass $(ASSETS)/stylesheets/app.scss $@ --style compressed

$(STATIC)/js/combined.min.js: $(ASSETS)/js/jquery-3.1.1.min.js $(ASSETS)/vendor/bootstrap-sass-3.3.7/assets/javascripts/bootstrap.min.js
	cat $^ > $@

.PHONY: bootstrap_static_fonts
bootstrap_static_fonts:
	mkdir -p $(STATIC)/fonts/bootstrap
	cp $(ASSETS)/vendor/bootstrap-sass-3.3.7/assets/fonts/bootstrap/* $(STATIC)/fonts/bootstrap/

.PHONY: clean
clean:
	rm -f $(STATIC)/css/combined.min.css
	rm -f $(STATIC)/js/combined.min.js
	rm -f $(STATIC)/fonts/bootstrap/*


.PHONY: test
test:
	./manage.py test -v 3 --failfast

.PHONY: run
run:
	./manage.py runserver 0.0.0.0:8000

.PHONY: dumpdb
dumpdb: latest.sql
       echo 'Now do vagrant ssh, then: dropdb vagrant && createdb vagrant && psql < latest.sql'

latest.dump:
	heroku pg:backups capture --app thinkingweekly
	curl -o latest.dump `heroku pg:backups public-url --app thinkingweekly`

latest.sql: latest.dump
	# convert dump file to SQL
	pg_restore --no-acl --no-owner -f latest.sql latest.dump
