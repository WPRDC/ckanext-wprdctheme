"use strict";

console.log('👋', ckan)
ckan.module('wprdc_theme_popover', function ($) {
  return {
    initialize: function () {
      console.log("I've been initialized for element: ", this.el);
    }
  };
});