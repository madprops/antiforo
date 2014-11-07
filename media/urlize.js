!(function(global) {

var wrap = function($) {
  var tlds = 'biz|cat|com|edu|gov|int|mil|net|org|pro|tel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cw|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw'

  // Adapted from Django's URLValidator
  // https://github.com/django/django/blob/stable/1.5.x/django/core/validators.py

  var urlPattern = new RegExp('(?:(?:http|ftp)s?://)?' + // optional scheme
    '(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:(' + tlds + ')(?!\\w)\\.?)|' +  // domain
    'localhost|' + // localhost
    '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}?)' + // or ipv4
    '(?::\\d+)?' +  // optional port
    '(?:[/?]?\\S+)?', 'gi');

  var schemelessPattern = new RegExp('href="((?!https?://).*?)"', 'gi');

  function urlize(s) {
    var _s = s.replace(urlPattern, function($1) {
      return '<a target="_blank" href="' + $1 + '">' + $1 + '</a>';
    });

    // If a URL doesn't include a scheme, insert 'http://'
    return _s.replace(schemelessPattern, function($1, $2) {
      return 'href="http://' + $2 + '"';
    });
  }

  $.fn.urlize = function(options) {
    if(typeof options === 'string') {
      return urlize(options);
    }
    return this.each(function() {
       $this = $(this);
       $this.html( urlize($this.html()) );
    });
  };
};

if ( typeof define === "function" && define.amd ) {
  define( "jquery-urlize", ['jquery'], wrap);
} else {
  wrap(global.jQuery);
}
})(this);