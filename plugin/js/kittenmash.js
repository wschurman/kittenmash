;(function($, window, document, undefined) {

  var defaults = {
    statusElement : null // jQuery element
  };

  function KittenMash(element, options) {
    this.element = element;
    this.$element = $(element);
    this.options = $.extend({}, defaults, options);

    this._defaults = defaults;
    this._name = 'kittenMash';

    this.init();
  }

  $.extend(KittenMash.prototype, {

    init: function() {

      if (!this.options['statusElement']) {
        $.error('Must supply a \'statusElement\' in the kittenmash options');
      }

      return this.$element.bind(
        'keypress.kittenmash',
        this.keyPressed.bind(this)
      );
    },

    destroy : function() {
      return this.$element.unbind('.kittenmash');
    },

    keyPressed : function(event) {
      this.options['statusElement'].text(this.$element.val());
    }

  });

  $.fn.kittenMash = function(method) {

    var args = Array.prototype.slice.call(arguments, 0)[0];
    return this.each(function() {

      if (!$.data(this, 'plugin_kittenMash')) {
        $.data(
          this,
          'plugin_kittenMash',
          new KittenMash(this, args)
        );
      }

      var km = $.data(this, 'plugin_kittenMash');

      if (km[method]) {
        return km[method].apply(this, Array.prototype.slice.call(arguments, 1))
      } else if (typeof method === 'object' || !method) {
        return this;
      } else {
        $.error('Method ' +  method + ' does not exist in jQuery.kittenmash');
      }

    });
  }
})(jQuery, window, document);
