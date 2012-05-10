/* DO NOT MODIFY. This file was compiled Tue, 26 Jul 2011 18:21:19 GMT from
 * /Users/justin/dev/lrr/rails/portlandcrime/app/coffee/neighborhoods.coffee
 */

(function() {
  $(function() {
    var darkstyle, lightstyle, load, map, mapel, path, po, svg;
    mapel = $('#neighborhoods-map');
    if (mapel.length === 0) {
      return;
    }
    path = $(document.body).data().path;
    po = org.polymaps;
    lightstyle = 5870;
    darkstyle = 1960;
    svg = po.svg('svg');
    map = po.map().container(mapel[0].appendChild(svg)).center({
      lat: -26.504682,
      lon: -49.091034
    }).zoom(13).zoomRange([9, 17]).add(po.interact()).add(po.hash());
    map.add(po.image().url(po.url("http://tiles.3geo.com.br/tiles/osm/{Z}/{X}/{Y}.png").hosts(['a.', 'b.', 'c.', ''])));
    $.getJSON("" + document.location.pathname + ".geojson", function(data) {
      return map.add(po.geoJson().features(data.features).on('load', load));
    });
    return load = function(e) {
      return $.each(e.features, function() {
        var el, label, props;
        el = $(this.element);
        props = this.data.properties;
        label = po.svg('text');
        el.addSVGClass('nhood');
        el.mouseover(function() {
          return el.addSVGClass('over');
        });
        el.mouseout(function() {
          return el.removeSVGClass('over');
        });
        return el.bind('click', {
          props: props,
          geo: this.data.geometry
        }, function(event) {
          return document.location = "/bairros/" + event.data.props.permalink;
        });
      });
    };
  });
}).call(this);
