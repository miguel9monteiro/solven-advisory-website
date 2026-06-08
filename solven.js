/* Solven Advisory — interaction layer
   Reveal strategy: content is visible by default. We mark only the elements
   that START below the fold as .pending (hidden), then add .in as they scroll
   into view. Above-the-fold content is never hidden, so it always paints and
   screenshots cleanly. A safety timeout guarantees nothing stays hidden. */
(function () {
  "use strict";

  /* ---- Mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Hero intro (transition-based, never leaves content hidden) ---- */
  if (!reduce && document.body.hasAttribute("data-intro")) {
    var b = document.body;
    b.classList.add("intro-armed");           // hide instantly (no transition)
    var release = function () { b.classList.add("intro-go"); };
    // Paint the hidden state once, then release so the transition runs.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(release);
    });
    // Guarantees: release even if rAF is throttled, so content always appears.
    window.setTimeout(release, 90);
    window.setTimeout(release, 1200);
    // Hard safety: snap to the visible resting state if the transition clock
    // never advances (real browsers finish the entrance long before this).
    window.setTimeout(function () { b.classList.add("intro-rescue"); }, 2000);
  }

  if (reduce) return; // remaining motion is enhancement only

  var all = Array.prototype.slice.call(
    document.querySelectorAll(".reveal, .draw-rule")
  );
  var vh = window.innerHeight || document.documentElement.clientHeight;

  // Only animate elements that begin below the fold. Above-the-fold stays
  // visible (and gets .in instantly so there's no flash).
  var pending = [];
  all.forEach(function (el) {
    var top = el.getBoundingClientRect().top;
    if (top > vh * 0.85) {
      el.classList.add("pending");
      pending.push(el);
    }
  });

  function reveal(el) {
    el.classList.add("in");
  }

  function check() {
    var h = window.innerHeight || document.documentElement.clientHeight;
    var trigger = h * 0.88;
    for (var i = pending.length - 1; i >= 0; i--) {
      var el = pending[i];
      var rect = el.getBoundingClientRect();
      if (rect.top < trigger && rect.bottom > 0) {
        reveal(el);
        pending.splice(i, 1);
      }
    }
    if (pending.length === 0) {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    }
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { check(); ticking = false; });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  check();

  // Safety net: never leave anything hidden.
  window.setTimeout(function () {
    pending.slice().forEach(reveal);
    pending.length = 0;
  }, 2500);

  /* ---- Subtle parallax on background chevrons (cinematic depth) ---- */
  var px = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (px.length) {
    var pxTicking = false;
    function pxUpdate() {
      var vh2 = window.innerHeight || document.documentElement.clientHeight;
      px.forEach(function (el) {
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.06;
        // measure the (untransformed) positioned parent to avoid feedback
        var anchor = el.offsetParent || el.parentElement;
        var rect = anchor.getBoundingClientRect();
        var offset = (rect.top + rect.height / 2 - vh2 / 2);
        el.style.transform = "translate3d(0," + (-offset * speed).toFixed(1) + "px,0)";
      });
    }
    window.addEventListener("scroll", function () {
      if (pxTicking) return;
      pxTicking = true;
      window.requestAnimationFrame(function () { pxUpdate(); pxTicking = false; });
    }, { passive: true });
    window.addEventListener("resize", pxUpdate);
    pxUpdate();
  }
})();
