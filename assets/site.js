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
