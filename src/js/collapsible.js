/*
 * Collapsible v1.1
 * https://github.com/Iteneo/Collapsible
 * MIT License
 */

(function($) {

  // init
  $.fn.collapsible = function(params) {

    if(!this || this.lenght < 1) {
      return this;
    }

    return createCollapsible(this, params);

  };

  // create the initial collapsible
  function createCollapsible(obj, params)
  {
    var opts = $.extend({}, $.fn.collapsible.defaults, params);

    obj.each(function() {

      $(this).find(classSelector(opts.classContainer)).each(function() {

        $(this).find(classSelector(opts.classHead)).bind('click', function(e) {

          var $this = $(this).parent(classSelector.classContainer);

          e.preventDefault();
          toggle($this, opts);

        });

        close($(this), opts);

      });

    });

  }

  function toggle($this, opts)
  {
    if(collapsed($this, opts)) {

      open($this, opts);

    } else {

      close($this, opts);

    }

    return false;
  }

  function collapsed($this, opts)
  {
    return $this.hasClass(opts.classClose);
  }

  function close($this, opts)
  {
    $this
      .addClass(opts.classClose)
      .removeClass(opts.classOpen);

    $this
      .find(classSelector(opts.classContent))
      .slideUp(opts.speed);
  }

  function open($this, opts)
  {
    closeAll($this, opts);

    $this
      .addClass(opts.classOpen)
      .removeClass(opts.classClose);

    $this
      .find(classSelector(opts.classContent))
      .slideDown(opts.speed);
  }

  // close all except $this
  function closeAll($this, opts)
  {
    $this.parent().find(classSelector(opts.classContainer)).not($this).each(function() {

      close($(this), opts);

    });
  }

  function classSelector(classname)
  {
    return "." + classname;
  }

  // opts
  $.fn.collapsible.defaults = {
    classContainer: "collapse-container",
    classHead     : "collapse-head",
    classContent  : "collapse-content",
    classOpen     : "collapse-open",
    classClose    : "collapse-close",
    speed         : 200
  };

})(jQuery);
