(function() {
  $(function() {
    if ($('body[data-path=trends-index]').length !== 0) {

      return $.getJSON('/trends.json', function(data) {
        var drawTrend, h, lblwid, mlabels, months, pb, pl, pr, pt, w, weeks, year, _ref;
        weeks = data[0], months = data[1];
        mlabels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
        year = new Date().getUTCFullYear();
        _ref = [30, 30, 20, 40], pt = _ref[0], pl = _ref[1], pb = _ref[2], pr = _ref[3];
        lblwid = 60;
        w = $('#trends').width() - (pl + pr + 10);
        h = 230 - (pt + pb);
        drawTrend = function(el, data) {
          var g, labels, legend, rules, samples, vis, wmax, x0, x1, y;
          samples = data[0].values.length;
          wmax = d3.max(data, function(d) {
            return d3.max(d.values, function(e) {
              return e.value;
            });
          });
          y = d3.scale.linear().domain([0, wmax]).range([h, 0]);
          x0 = d3.scale.ordinal().domain(d3.range(samples)).rangeBands([0, w], 0.5);
          x1 = d3.scale.ordinal().domain(d3.range(2)).rangeRoundBands([0, x0.rangeBand()]);
          labels = el === '#monthly' ? mlabels : d3.range(samples);
          vis = d3.select(el).append('svg:svg').attr('width', w + (pl + pr)).attr('height', h + pt + pb).attr('class', 'viz').append('svg:g').attr('transform', "translate(" + pl + "," + pt + ")");
          rules = vis.selectAll('g.rule').data(function(d) {
            if (el !== '#monthly') {
              return y.ticks(10);
            } else {
              return y.ticks(4);
            }
          }).enter().append('svg:g').attr('class', function(d) {
            if (d) {
              return null;
            } else {
              return 'axis';
            }
          });
          rules.append('svg:line').attr("y1", function(d) {
            return Math.ceil(y(d));
          }).attr("y2", function(d) {
            return Math.ceil(y(d));
          }).attr("x1", 0).attr("x2", w);
          rules.append('svg:text').attr('y', y).attr("dy", ".2em").attr('x', w + 5).attr('class', 'vlbl').text(function(d) {
            return d;
          });
          vis.selectAll('h.text').data(labels).enter().append('svg:text').attr('class', function(d, i) {
            if (i % 2 !== 0 && el !== '#monthly') {
              return 'hlbl hide';
            } else {
              return 'hlbl';
            }
          }).attr("transform", function(d, i) {
            return "translate(" + (x0(i)) + ",0)";
          }).attr("x", x0.rangeBand()).attr("y", h + 12).attr("text-anchor", "middle").text(function(d) {
            if (el !== '#monthly') {
              return d + 1;
            } else {
              return d;
            }
          });
          legend = vis.selectAll('legend').data([year - 1, year]);
          legend.enter().append('svg:circle').attr('transform', "translate(" + ((w - (lblwid * 2)) / 2) + ", -10)").attr('cx', function(d, i) {
            return lblwid * i;
          }).attr('fill', function(d) {
            if (d === year) {
              return '#00b2ec';
            } else {
              return '#cccccc';
            }
          }).attr('class', 'c').attr('r', 4).text(function(d) {
            return d;
          });
          legend.enter().append('svg:text').attr('transform', "translate(" + ((w - (lblwid * 2)) / 2) + ", -10)").attr("x", function(d, i) {
            return 10 + (lblwid * i);
          }).attr('y', 5).attr('class', 'legend').text(function(d) {
            return d;
          });
          g = vis.selectAll('g.bar').data(data).enter().append('svg:g').attr('fill', function(d) {
            if (d.series === 'prev') {
              return '#cccccc';
            } else {
              return '#00b2ec';
            }
          }).attr('transform', function(d, i) {
            return "translate(" + (x1(i)) + ",0)";
          });
          return g.selectAll('rect').data(function(d) {
            return d.values;
          }).enter().append('svg:rect').attr('transform', function(d, i) {
            return "translate(" + (x0(i) + x1.rangeBand()) + ",0)";
          }).attr('width', x1.rangeBand() / 2).attr('height', function(d, i) {
            return h - y(d.value);
          }).attr('y', function(d) {
            return y(d.value);
          });
        };
        drawTrend('#weekly', weeks);
        return $(document).bind('tab.clicked', function(event, el) {
          var hdr, sel;
          el = $(el);
          sel = $('li a.current').attr('href');
          hdr = el.prev('h1');
          if (sel === '#monthly') {
            return hdr.text('Estatística semanal');
          } else {
            hdr.text('Estatística mensal');
            if ($('#monthly svg').length === 0) {
              return drawTrend('#monthly', months);
            }
          }
        });
      });
    }
  });
}).call(this);
