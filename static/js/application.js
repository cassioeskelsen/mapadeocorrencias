
$.fn.slideFadeToggle = function(speed, callback, easing) {
  return this.animate({height: 'toggle'}, speed, easing, callback);
}

$(function() {  
  $("ul.segments").tabs("div.pane").bind('onClick', function() {
    $(document).trigger('tab.clicked', this);
  });
       
  /**
   * Setup all the interactions for enabling and disabling offenses and
   * complete groups of delito types
   */
  var checks = $('span.check')
  checks.click(function() {
    var check = $(this),
        iac = 'inactive'
    
    if(check.hasClass('group')) {
      var li = check.closest('li.group'),
          children = li.find('span.check')
          
      if(check.hasClass(iac)) {
        check.removeClass(iac)
        children.removeClass(iac)
      } else {
        check.addClass(iac)
        children.addClass(iac)
      }
    } else {
      if(check.hasClass(iac)) {
        check.removeClass(iac)
          .closest('li.group')
          .find('span.group')
          .removeClass(iac)
      } else {
        check.addClass(iac)
      }
    }

    $('#map').trigger('map.togglecrimes')
  })
  
  /**
   * Expand and collapse of delito groups
   */
  $('span.exp, span.otype a').click(function(event) {
    event.stopPropagation()
    event.preventDefault()
    var el = $(this)
    var child = el.closest('li').find('ul.offenses')
    if(!el.hasClass('exp'))
      el = el.siblings('span.exp')
      
    el.toggleClass('collapsed')
    
    child.animate({height: 'toggle'}, 'slow', 'easeOutBack')
  })
  
  $('ol.alpha-list li a').click(function() {
    var el     = $(this).attr('href'),
        offset = $(el).offset().top
        
    $('html,body').animate({scrollTop: offset}, 500, 'easeOutQuad')
  })
  
  $(document).bind('crimes.loaded', function(event, data) {
$('#total .num').text(data.features.length)
    return //todo

    if($('body[data-path=delitos-show]').length != 1)
      return


    var start = Date.today().add(-30).days(),
        end = new Date(),
        range = d3.range(start.getTime(), end.getTime(), 86400000 /* 1 day */),
        hash = {},
        counts = [],
        nhoods = {},
        nhcounts = []

    $.each(range, function() {
       var d = new Date(this)
       hash[d.toString('MM-dd-yy')] = 0
    })

    $.each(data.features, function() {
      var props = this.properties,
          ra = Date.parse(this.properties.reportado)//,
         // nhood = nhoods[props.neighborhood_id]
      return;
      if(!nhood)
          nhoods[props.neighborhood_id] = 0
      
      nhoods[props.neighborhood_id]++
      hash[ra.toString('MM-dd-yy')]++     
    })

  
   for(var date in hash)
     counts.push(hash[date])
     
     sparkline('#pulse', counts, true) 
     $('#pulse').append($('<span />').text('30 Day Trend').addClass('quiet'))  
     $('#total .num').text(data.features.length)
     
     var last = Date.parse(data.features[0].properties.reported_at) 
     $('#lastreport .val').text(last.toString('ddd MMM, dd yyyy hh:mmtt'))
     
    /**
     * Right now the neighborhood names aren't stored on crimes because of future 
     * plans to store the polygon data for neighborhoods.  Because of this, I'm 
     * finding the top 5 neighborhoods via js and requesting their names.
     *
     * I'm considering creating a NeighborhoodGeo class that would store the geo
     * data and including the names in the delito document and adding a one to one
     * relationship with the delito model (@delito.neighborhood_geo).
     */ 
     for(var nhid in nhoods)
       nhcounts.push([nhid, nhoods[nhid]])

     nhcounts.sort(function(a, b) {
       return (b[1] < a[1]) ? -1 : ((b[1] > a[1]) ? 1 : 0)
     })
     
     var top5 = nhcounts.slice(0,5),
         nhids = top5.map(function(ar) { return ar[0] }),
         off
     
    $.getJSON(document.location.pathname + '/recurring_neighborhoods.json?ids[]=' + nhids.join(','), function(data) {
      var ul = $('#topneighborhoods ul.val'),
          names = []
                  
      $.each(data, function() {
        var nhood = this,
            cnt = $.grep(top5, function(nhc, idx) { 
              return nhc[0] == nhood.id 
            })[0]
        
        //console.log(nhood) 
        //if(cnt)
          names.push({name: this.name.capitalizeWords(), count: cnt[1], permalink: this.permalink})
      })
      
      names = names.sort(function(a, b) {
        return (b['count'] < a['count']) ? -1 : ((b['count'] > a['count']) ? 1 : 0)
      })
      
      $.each(names, function() {
        this.name == ' ' ? this.name = 'Unknown' : this.name
        ul.append($('<li />')
          .html($('<a />').attr('href', '/neighborhoods/' + this.permalink).text(this.name.capitalizeWords()))
          .append($('<span />')
            .addClass('count')
            .text(this.count)))
      })
    })
  })
});