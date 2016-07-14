"use strict";

// http://stackoverflow.com/a/17448504
(function(window){
  var app = {};


app.attachStationSuggestions = function() {

  var searchIndex = lunr(function () {
    this.field('three_alpha', {boost: 10})
    this.field('name', {boost: 10}),
    this.ref('name')
  });

  this.getJSON("/api/stations/", function(data) {
    data.forEach(function(station) {
      searchIndex.add(station);
    }, this);

    console.log('Built search index.');
    app.attachChangeHandlers(searchIndex);
  });
};

function StationInputHandler(stationInput, stationSearchIndex) {
  var o = {};
  o.stationInput = stationInput;
  o.stationSearchIndex = stationSearchIndex;
  o.suggestionsUl = document.querySelector('#' + stationInput.id + '_suggestions');
  o.dropdownDiv = document.querySelector('#' + stationInput.id + '_dropdown');

  o.connect = function() {
    this.stationInput.oninput = this.handleInputChange;
  };

  o.handleInputChange = function(event) {
    var results = [];

    if(event.target.value.length < 3) {
      results = []
    }
    else {
      results = this.stationSearchIndex.search(event.target.value);
    }
    this.displaySuggestionsDropdown(results);
  }.bind(o);

  o.displaySuggestionsDropdown = function(results) {
      if(results.length) {
        this.dropdownDiv.classList.add('open');
      }
      else {
        this.dropdownDiv.classList.remove('open');
      }

      while(this.suggestionsUl.firstChild) {
        this.suggestionsUl.removeChild(this.suggestionsUl.firstChild);
      }

      results.forEach(function(searchResult) { // create <li> for each result
        var liTag = document.createElement('li'),
            aTag = document.createElement('a'),
            text = document.createTextNode(searchResult.ref);
        aTag.href = '#';
        liTag.appendChild(aTag);
        aTag.appendChild(text);

        aTag.onclick = function(clickEvent) {
          this.stationInput.value = clickEvent.target.text;
          this.dropdownDiv.classList.remove('open');
        }.bind(this);
        this.suggestionsUl.appendChild(liTag);
      }.bind(this)
      );
  };

  o.connect();
  return o
};



app.stationInputHandlers = [];

app.attachChangeHandlers = function(searchIndex) {
  var stationInputs = Array(),
      suggestionsUl = null,
      dropdownDiv = null,

      results = [];

  Array.prototype.forEach.call(
      document.querySelectorAll('input[data-input-type="station"]'),
      function(node) {
        stationInputs.push(node);
      });

  stationInputs.forEach(function(stationInput) {
    app.stationInputHandlers.push(
      StationInputHandler(stationInput, searchIndex));
  }, this);

};


app.getJSON = function(url, successHandler, errorHandler) {
  var xhr = typeof XMLHttpRequest != 'undefined'
    ? new XMLHttpRequest()
    : new ActiveXObject('Microsoft.XMLHTTP');
  xhr.open('get', url, true);
  xhr.onreadystatechange = function() {
    var status, data;
    // https://xhr.spec.whatwg.org/#dom-xmlhttprequest-readystate
    if (xhr.readyState == 4) { // `DONE`
      status = xhr.status;
      if (status == 200) {
        data = JSON.parse(xhr.responseText);
        successHandler && successHandler(data);
      } else {
        errorHandler && errorHandler(status);
      }
    }
  };
  xhr.send();
};

app.loadPage = function() {
  console.log(document.body.dataset.title);
  switch(document.body.dataset.runJavascript) {
    case "attach-station-suggestions" :
      app.attachStationSuggestions();
      break;
    }
};

window.app = app;
})(window);

app.loadPage();
