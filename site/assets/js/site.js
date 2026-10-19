/* QUAKE Gym & Pilates — small site script: mobile menu + contact click tracking. */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // Click tracking. Links carry data-track="click_whatsapp|click_phone|click_maps|click_instagram".
  // Events go to the dataLayer (Google Tag Manager) and to gtag (GA4) if either is installed.
  window.dataLayer = window.dataLayer || [];
  document.addEventListener("click", function (e) {
    var link = e.target.closest("[data-track]");
    if (!link) return;
    var params = {
      link_url: link.href || "",
      link_location: link.getAttribute("data-track-location") || "",
      page_language: document.documentElement.lang
    };
    window.dataLayer.push(Object.assign({ event: link.getAttribute("data-track") }, params));
    if (typeof window.gtag === "function") window.gtag("event", link.getAttribute("data-track"), params);
  });

  // Footer year
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());
})();
