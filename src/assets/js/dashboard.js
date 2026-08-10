/* ==========================================================================
   /dashboard/ — what the site is actually doing
   Reads the first-party event log written by site.js. If an analytics
   endpoint is configured it pulls aggregates from there instead, so this
   becomes a real cross-visitor dashboard rather than a QA view.
   ========================================================================== */
(function () {
  "use strict";
  var CC = window.CCHA || {};
  var CFG = CC.config || {};
  var $ = function (s) { return document.querySelector(s); };

  var LABEL = {
    call_click: "Phone call started",
    text_click: "Text message started",
    form_submit: "Form submitted",
    book_click: "Booking button",
    scrub_used: "Used the temperature dial",
    scroll_depth: "Scroll depth",
    page_view: "Page view",
    scroll_to_form: "Jumped to form",
    review_outbound: "Clicked through to Google",
    nav_services: "Opened services",
  };
  var SOURCE = {
    google_ads: "Google Ads", google_organic: "Google (organic)", bing_ads: "Bing Ads",
    search_other: "Other search", meta: "Facebook / Instagram", social: "Social",
    yelp: "Yelp", nextdoor: "Nextdoor", direct: "Direct / typed in",
  };
  var pretty = function (m, k) { return m[k] || (k || "").replace(/[:_]/g, " "); };

  function tally(rows, key) {
    var m = {};
    rows.forEach(function (r) { var v = r[key] || "—"; m[v] = (m[v] || 0) + 1; });
    return Object.keys(m).map(function (k) { return [k, m[k]]; })
                 .sort(function (a, b) { return b[1] - a[1]; });
  }

  function barTable(el, rows, map, headA, headB) {
    if (!rows.length) { el.innerHTML = '<p style="color:var(--steel)">Nothing recorded yet.</p>'; return; }
    var max = rows[0][1];
    el.innerHTML =
      '<table class="tbl"><thead><tr><th>' + headA + '</th><th style="width:40%">' + headB +
      '</th><th style="text-align:right">Count</th></tr></thead><tbody>' +
      rows.map(function (r) {
        return '<tr><td>' + pretty(map, r[0]) + '</td>' +
               '<td><div class="bar"><i style="width:' + (r[1] / max * 100) + '%"></i></div></td>' +
               '<td style="text-align:right;font-family:var(--mono)">' + r[1] + "</td></tr>";
      }).join("") + "</tbody></table>";
  }

  function render(rows) {
    var leads = rows.filter(function (r) {
      return r.event === "call_click" || r.event === "form_submit" || r.event === "text_click";
    });
    var views = rows.filter(function (r) { return r.event === "page_view"; });
    var rate = views.length ? (leads.length / views.length * 100).toFixed(1) : "0.0";

    $("#s-leads").textContent = leads.length;
    $("#s-calls").textContent = rows.filter(function (r) { return r.event === "call_click"; }).length;
    $("#s-forms").textContent = rows.filter(function (r) { return r.event === "form_submit"; }).length;
    $("#s-views").textContent = views.length;
    $("#s-rate").textContent = rate + "%";

    barTable($("#t-source"), tally(leads, "last_source"), SOURCE, "Where the lead came from", "");
    barTable($("#t-cta"), tally(leads.filter(function (r) { return r.link_location; }), "link_location"),
             {}, "Which button they tapped", "");
    barTable($("#t-page"), tally(leads, "page"), {}, "Page they were on", "");
    barTable($("#t-event"), tally(rows, "event"), LABEL, "Every event", "");

    var recent = rows.slice(-40).reverse();
    $("#t-recent").innerHTML = recent.length
      ? '<table class="tbl"><thead><tr><th>When</th><th>Event</th><th>Page</th><th>Source</th></tr></thead><tbody>' +
        recent.map(function (r) {
          var cls = r.event === "call_click" ? "tag--call" : r.event === "form_submit" ? "tag--form" : "";
          return "<tr><td>" + new Date(r.ts).toLocaleString() +
                 '</td><td><span class="tag ' + cls + '">' + pretty(LABEL, r.event) + "</span></td><td>" +
                 (r.page || "—") + "</td><td>" + pretty(SOURCE, r.last_source) + "</td></tr>";
        }).join("") + "</tbody></table>"
      : '<p style="color:var(--steel)">No events yet. Open the site in another tab, tap a call button, then come back.</p>';
  }

  function boot() {
    var note = $("#dash-note");
    if (CFG.analyticsEndpoint) {
      fetch(CFG.analyticsEndpoint + "?summary=1", { headers: { Accept: "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          note.textContent = "Live data from all visitors.";
          render(d.events || []);
        })
        .catch(function () {
          note.textContent = "Couldn't reach the analytics endpoint — showing this device only.";
          render(CC.readEvents ? CC.readEvents() : []);
        });
    } else {
      note.textContent = "Showing this browser only. Connect an endpoint for all-visitor data — see the README.";
      render(CC.readEvents ? CC.readEvents() : []);
    }
  }

  var clear = $("#dash-clear");
  if (clear) clear.addEventListener("click", function () {
    if (confirm("Clear the locally recorded events on this device?")) {
      if (CC.clearEvents) CC.clearEvents();
      location.reload();
    }
  });

  boot();
})();
