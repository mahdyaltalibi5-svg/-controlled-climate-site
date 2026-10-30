/* ==========================================================================
   Controlled Climate Heating & Air — site behaviour
   1. Lead-source attribution (first-touch + last-touch, survives sessions)
   2. Conversion event tracking (calls, texts, form submits)
   3. Dynamic number insertion hook (swap in a call-tracking number later)
   4. Nav, scroll reveal, form submit
   No dependencies. ~4kb.
   ========================================================================== */
(function () {
  "use strict";

  document.documentElement.classList.add("js");

  window.dataLayer = window.dataLayer || [];
  var CC = (window.CCHA = window.CCHA || {});
  var CFG = CC.config || {};

  /* ---------------------------------------------------------------------
     1. ATTRIBUTION
     Answers "where did this lead come from" even when the customer clicks
     an ad in July and calls in September. Stored first-party in
     localStorage; both first touch and last touch travel with the lead.
     --------------------------------------------------------------------- */
  var KEY_FIRST = "ccha_first_touch";
  var KEY_LAST = "ccha_last_touch";
  var PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
                "gclid", "wbraid", "gbraid", "fbclid", "msclkid"];

  function store(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function read(k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } }

  function classify(ref, qs) {
    if (qs.gclid || qs.wbraid || qs.gbraid) return "google_ads";
    if (qs.msclkid) return "bing_ads";
    if (qs.fbclid) return "meta";
    if (qs.utm_source) return String(qs.utm_source).toLowerCase();
    if (!ref) return "direct";
    var h = "";
    try { h = new URL(ref).hostname.replace(/^www\./, ""); } catch (e) { return "referral"; }
    if (h.indexOf(location.hostname.replace(/^www\./, "")) === 0) return "internal";
    if (/google\./.test(h)) return "google_organic";
    if (/bing\.|duckduckgo|yahoo\./.test(h)) return "search_other";
    if (/facebook|instagram|fb\.com/.test(h)) return "social";
    if (/nextdoor/.test(h)) return "nextdoor";
    if (/yelp/.test(h)) return "yelp";
    return "referral:" + h;
  }

  function captureTouch() {
    var qs = {};
    new URLSearchParams(location.search).forEach(function (v, k) { qs[k] = v; });
    var picked = {};
    PARAMS.forEach(function (p) { if (qs[p]) picked[p] = qs[p]; });

    var touch = {
      source: classify(document.referrer, qs),
      referrer: document.referrer || "",
      landing: location.pathname + location.search,
      ts: new Date().toISOString(),
      params: picked
    };

    if (touch.source === "internal") return; // don't overwrite on internal navigation
    if (!read(KEY_FIRST)) store(KEY_FIRST, touch);
    store(KEY_LAST, touch);
  }
  captureTouch();

  CC.attribution = function () {
    var f = read(KEY_FIRST) || {}, l = read(KEY_LAST) || {};
    return {
      first_source: f.source || "direct",
      first_landing: f.landing || "",
      first_seen: f.ts || "",
      last_source: l.source || "direct",
      last_landing: l.landing || "",
      gclid: (l.params && l.params.gclid) || (f.params && f.params.gclid) || "",
      utm_campaign: (l.params && l.params.utm_campaign) || "",
      page: location.pathname
    };
  };

  /* ---------------------------------------------------------------------
     2. EVENTS
     Every conversion action pushes to dataLayer with attribution attached,
     so GA4 / GTM / Ads all see the same shape.
     --------------------------------------------------------------------- */
  function track(event, extra) {
    var payload = Object.assign({ event: event }, CC.attribution(), extra || {});
    window.dataLayer.push(payload);
    if (typeof gtag === "function" && CFG.adsConversion && event === "call_click") {
      gtag("event", "conversion", { send_to: CFG.adsConversion });
    }
    if (CFG.debug) console.log("[track]", payload);
  }
  CC.track = track;

  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("tel:") === 0) {
      track("call_click", { link_location: a.dataset.loc || "unknown", phone: href.slice(4) });
    } else if (href.indexOf("sms:") === 0) {
      track("text_click", { link_location: a.dataset.loc || "unknown" });
    } else if (a.dataset.track) {
      track(a.dataset.track, { link_location: a.dataset.loc || "unknown" });
    }
  });

  /* Scroll depth — tells you whether people read or bounce, per page. */
  var hit = {};
  window.addEventListener("scroll", function () {
    var d = document.documentElement;
    var pct = (window.scrollY + window.innerHeight) / d.scrollHeight * 100;
    [50, 75, 90].forEach(function (m) {
      if (pct >= m && !hit[m]) { hit[m] = 1; track("scroll_depth", { depth: m }); }
    });
  }, { passive: true });

  /* ---------------------------------------------------------------------
     3. DYNAMIC NUMBER INSERTION
     When a call-tracking number is added later, set
     window.CCHA.config.trackingNumbers = { google_ads: {display, e164}, ... }
     Nothing in the HTML has to change.
     --------------------------------------------------------------------- */
  CC.applyNumbers = function () {
    var map = CFG.trackingNumbers;
    if (!map) return;
    var src = CC.attribution().last_source;
    var n = map[src] || map["default"];
    if (!n) return;
    document.querySelectorAll("[data-phone]").forEach(function (el) {
      if (el.tagName === "A") el.setAttribute("href", "tel:" + n.e164);
      if (el.dataset.phone === "display") el.textContent = n.display;
    });
  };
  CC.applyNumbers();

  /* ---------------------------------------------------------------------
     4. UI
     --------------------------------------------------------------------- */
  var burger = document.querySelector(".burger");
  var nav = document.getElementById("nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* --- scroll progress: the hot→cold seam fills as you read --------------- */
  var bar = document.querySelector(".progress");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ticking = false;

  function onFrame() {
    var d = document.documentElement;
    var max = d.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? window.scrollY / max : 0) + ")";

    /* parallax: elements drift against the scroll at their own rate */
    if (!reduce) {
      px.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
        var progress = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
        el.style.transform = "translate3d(0," + (progress * el._rate).toFixed(2) + "px,0)";
      });
    }
    ticking = false;
  }

  var px = [].slice.call(document.querySelectorAll("[data-px]"));
  px.forEach(function (el) { el._rate = parseFloat(el.dataset.px) || 40; });

  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onFrame); }
  }, { passive: true });
  window.addEventListener("resize", onFrame, { passive: true });
  onFrame();

  /* --- scroll reveals, staggered by position within their group ----------- */
  var revealed = document.querySelectorAll(".rv, .rv-mask, .reveal-img");

  /* give siblings an increasing --i so they cascade instead of popping */
  document.querySelectorAll(".grid, .steps, .details, .faq, .intent__grid, .trust").forEach(function (group) {
    var i = 0;
    [].forEach.call(group.children, function (child) {
      var t = child.matches(".rv, .rv-mask, .reveal-img") ? child
            : child.querySelector(".rv, .rv-mask, .reveal-img");
      if (t) { t.style.setProperty("--i", Math.min(i, 5)); i++; }
    });
  });

  if (revealed.length && "IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    revealed.forEach(function (el) { io.observe(el); });
  } else {
    revealed.forEach(function (el) { el.classList.add("in"); });
  }

  /* --- tactile hover light ------------------------------------------------ */
  if (!reduce && window.matchMedia("(pointer: fine)").matches) {
    document.querySelectorAll(".card, .intent__item, .proof, .rev, .btn").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
        el.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
      });
      el.addEventListener("pointerleave", function () {
        el.style.removeProperty("--mx");
        el.style.removeProperty("--my");
      });
    });
  }

  /* --- counters: numbers tick up the first time they're seen -------------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target;
        var target = parseFloat(el.dataset.count);
        var dec = (el.dataset.count.split(".")[1] || "").length;
        if (dec > 0) {
          el.textContent = el.dataset.count;
          return;
        }
        var t0 = null;
        function step(t) {
          if (!t0) t0 = t;
          var k = Math.min((t - t0) / 900, 1);
          var eased = 1 - Math.pow(1 - k, 3);
          el.textContent = (target * eased).toFixed(dec);
          if (k < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------------------------------------------------------------------
     5. FORM
     Posts JSON to CFG.formEndpoint with attribution attached. Falls back to
     a mailto handoff if no endpoint is configured yet, so the form is never
     a dead end during the pre-launch window.
     --------------------------------------------------------------------- */
  document.querySelectorAll("form[data-lead]").forEach(function (form) {
    var note = form.querySelector(".form-note");
    var btn = form.querySelector("button[type=submit]");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector("[name=company]").value) return; // honeypot

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      delete data.company;
      Object.assign(data, CC.attribution());
      data.submitted_at = new Date().toISOString();

      function say(msg, ok) {
        if (!note) return;
        note.textContent = msg;
        note.className = "form-note " + (ok ? "is-ok" : "is-err");
      }

      if (!CFG.formEndpoint) {
        say("Online callback requests are not enabled yet. You can email this request using the link below or call " + (CFG.phoneDisplay || "") + ".", false); if(note) { var email = "andrewscogganhvac@gmail.com"; var subject = encodeURIComponent("Service request - Controlled Climate"); var body = encodeURIComponent(["Name: "+(data.name||""),"Phone: "+(data.phone||""),"Service: "+(data.service||""),"Details: "+(data.message||"")].join(String.fromCharCode(10))); var a=document.createElement("a"); a.href="mailto:"+email+"?subject="+subject+"&body="+body; a.textContent="Open email to send your request"; a.className="form-mail-fallback"; a.style.cssText="display:block;margin-top:10px;text-decoration:underline;font-weight:750;color:#e88d56"; note.appendChild(a); }
        console.warn("[CCHA] Set window.CCHA.config.formEndpoint — see README.");
        return;
      }

      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = "Sending…";

      fetch(CFG.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        track("form_submit", { form_name: form.dataset.lead, service: data.service || "" });
        if (CFG.thankYouUrl) { location.href = CFG.thankYouUrl; return; }
        form.reset();
        say("Got it. We'll call you back shortly — usually within the hour during business hours.", true);
      }).catch(function () {
        say("That didn't send. Call " + (CFG.phoneDisplay || "") + " and we'll get you on the schedule.", false);
      }).finally(function () {
        btn.disabled = false;
        btn.textContent = label;
      });
    });
  });
})();

/* ==========================================================================
   v3 — header state + the thermal scrub
   ========================================================================== */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- header condenses once you leave the top ---------------------------- */
  var hdr = document.querySelector(".hdr");
  if (hdr) {
    var stuck = false;
    var onScroll = function () {
      var should = window.scrollY > 24;
      if (should !== stuck) { stuck = should; hdr.classList.toggle("is-stuck", should); }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* --- thermal scrub ------------------------------------------------------
     One control that says what the business is: drag from cooling to heating
     and the imagery, copy, accent colour and service list all cross over.
     Pointer, keyboard and touch all drive the same --t custom property.
     ---------------------------------------------------------------------- */
  var scrub = document.querySelector("[data-scrub]");
  if (!scrub) return;

  var track = scrub.querySelector(".scrub__track");
  var tempEl = scrub.querySelector("[data-scrub-temp]");
  var modeEl = scrub.querySelector("[data-scrub-mode]");
  var titleEl = scrub.querySelector("[data-scrub-title]");
  var copyEl = scrub.querySelector("[data-scrub-copy]");
  var listEl = scrub.querySelector("[data-scrub-list]");

  var COLD = JSON.parse(scrub.dataset.cold);
  var HOT = JSON.parse(scrub.dataset.hot);

  var t = 0.5, raf = null, lastSide = null;

  function clampT(v) {
    v = Number(v);
    return Number.isFinite(v) ? Math.min(1, Math.max(0, v)) : 0.5;
  }

  function render() {
    t = clampT(t);
    scrub.style.setProperty("--t", t.toFixed(3));
    /* 62°F at full cold through 74°F at full hot — a thermostat range, not a gimmick */
    tempEl.textContent = Math.round(62 + t * 12) + "\u00B0";
    var side = t >= 0.5 ? HOT : COLD;
    if (side !== lastSide) {
      lastSide = side;
      modeEl.textContent = side.mode;
      titleEl.textContent = side.title;
      copyEl.textContent = side.copy;
      listEl.innerHTML = side.links
        .map(function (l) { return '<li><a href="' + l[1] + '">' + l[0] + "</a></li>"; })
        .join("");
    }
    track.setAttribute("aria-valuenow", Math.round(t * 100));
    track.setAttribute("aria-valuetext", side.mode);
  }

  function setFromX(clientX) {
    var r = track.getBoundingClientRect();
    t = r.width ? clampT((clientX - r.left) / r.width) : t;
    if (!raf) raf = requestAnimationFrame(function () { raf = null; render(); });
  }

  var dragging = false;
  track.addEventListener("pointerdown", function (e) {
    dragging = true; track.setPointerCapture(e.pointerId); setFromX(e.clientX);
  });
  track.addEventListener("pointermove", function (e) { if (dragging) setFromX(e.clientX); });
  ["pointerup", "pointercancel"].forEach(function (ev) {
    track.addEventListener(ev, function () {
      dragging = false;
      if (window.CCHA && window.CCHA.track) {
        window.CCHA.track("scrub_used", { side: t >= 0.5 ? "heating" : "cooling" });
      }
    });
  });

  track.addEventListener("keydown", function (e) {
    var step = e.shiftKey ? 0.2 : 0.05;
    if (e.key === "ArrowRight" || e.key === "ArrowUp") { t = clampT(t + step); }
    else if (e.key === "ArrowLeft" || e.key === "ArrowDown") { t = clampT(t - step); }
    else if (e.key === "Home") { t = 0; }
    else if (e.key === "End") { t = 1; }
    else return;
    e.preventDefault(); render();
  });

  /* settle from the middle out to cooling on first view, so it reads as movable */
  render();
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.disconnect();
        var t0 = null, from = t, to = 0.12;
        (function anim(ts) {
          if (!t0) t0 = ts;
          var k = Math.min((ts - t0) / 1100, 1);
          t = clampT(from + (to - from) * (1 - Math.pow(1 - k, 3)));
          render();
          if (k < 1) requestAnimationFrame(anim);
        })();
      });
    }, { threshold: 0.4 });
    io.observe(scrub);
  }
})();

/* ==========================================================================
   v3 — first-party event log
   Every tracked event is also written to a rolling local log so /dashboard/
   can show what's firing without waiting on GA4's 24-48h processing delay.
   If an analytics endpoint is configured, events are beaconed there too and
   the dashboard reads aggregates back from it.
   ========================================================================== */
(function () {
  "use strict";
  var CC = window.CCHA || {};
  var CFG = CC.config || {};
  var KEY = "ccha_events";
  var CAP = 400;

  function log(e) {
    try {
      var arr = JSON.parse(localStorage.getItem(KEY) || "[]");
      arr.push(e);
      if (arr.length > CAP) arr = arr.slice(-CAP);
      localStorage.setItem(KEY, JSON.stringify(arr));
    } catch (err) {}
  }
  CC.readEvents = function () {
    try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { return []; }
  };
  CC.clearEvents = function () { try { localStorage.removeItem(KEY); } catch (e) {} };

  /* wrap the existing tracker rather than replacing it */
  var inner = CC.track;
  CC.track = function (event, extra) {
    if (inner) inner(event, extra);
    var rec = Object.assign({ event: event, ts: Date.now() },
                            CC.attribution ? CC.attribution() : {}, extra || {});
    log(rec);
    if (CFG.analyticsEndpoint && navigator.sendBeacon) {
      try {
        navigator.sendBeacon(CFG.analyticsEndpoint,
          new Blob([JSON.stringify(rec)], { type: "application/json" }));
      } catch (e) {}
    }
  };

  /* page views count too */
  CC.track("page_view", { title: document.title });
})();
