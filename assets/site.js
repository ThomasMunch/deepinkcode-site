// Click-to-load YouTube: nothing is loaded from YouTube until the visitor presses play.
document.querySelectorAll('a.video[data-yt]').forEach(function (link) {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + link.dataset.yt + '?autoplay=1&rel=0';
    f.title = link.dataset.title || 'Video';
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    var wrap = document.createElement('div');
    wrap.className = 'video video-playing';
    wrap.appendChild(f);
    link.replaceWith(wrap);
  });
});

// Ad attribution without cookies: if the visitor came from an ad (utm_* or gclid in the URL),
// pass the source on to the store links so installs show up per campaign in
// Play Console (UTM) and App Store Connect (Campaigns). Nothing is stored or sent anywhere else.
(function () {
  var q = new URLSearchParams(location.search);
  var gclid = q.get('gclid');
  var src = q.get('utm_source') || (gclid ? 'google' : '');
  if (!src) return;
  var clean = function (s) { return String(s).replace(/[^A-Za-z0-9_.-]/g, '').slice(0, 40); };
  var med = clean(q.get('utm_medium') || (gclid ? 'cpc' : 'referral'));
  var camp = clean(q.get('utm_campaign') || 'none');
  src = clean(src);
  document.querySelectorAll('a.badge-gp').forEach(function (a) {
    var u = new URL(a.href);
    u.searchParams.set('referrer', 'utm_source=' + src + '&utm_medium=' + med + '&utm_campaign=' + camp);
    a.href = u.toString();
  });
  document.querySelectorAll('a.badge-as').forEach(function (a) {
    var u = new URL(a.href);
    if (!u.searchParams.has('pt')) return;
    u.searchParams.set('ct', (src + '-' + camp).slice(0, 40));
    a.href = u.toString();
  });
})();
