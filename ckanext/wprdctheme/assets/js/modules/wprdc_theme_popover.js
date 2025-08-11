"use strict";

const AGREEMENT_COOKIE_NAME = 'agreedTerms'

function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {``
  const nameEQ = name + "=";
  const ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

function eraseCookie(name) {
  document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 ÎGMT;';
}

ckan.module('wprdc_theme_popover', function ($) {
  return {
    initialize: function () {
      // todo: pass logged in user to this function so we can assume they agreed
      const hasAgreed = getCookie(AGREEMENT_COOKIE_NAME) === 'true';
      if (!hasAgreed) {
        const dialogEl = this.el[0]
        dialogEl.showModal();
        dialogEl.addEventListener('cancel', (event) => {
          event.preventDefault();
        });
        dialogEl.addEventListener('close', (e) => {
          console.log(e);
          setCookie(AGREEMENT_COOKIE_NAME, 'true');
        })
      }
    }
  };
});