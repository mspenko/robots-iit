/* Local glue for the preserved Weebly theme; no remote services. */
window.Code = {Util: {Events: {fire: function(element, name) {
  element.dispatchEvent(new MouseEvent(name, {bubbles: true, cancelable: true}));
}}}};
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.desktop-nav .wsite-menu-item-wrap').forEach(function (item) {
    const menu = item.querySelector('.wsite-menu-wrap');
    if (!menu) return;
    function show() { menu.style.display = 'block'; }
    function hide() { menu.style.display = 'none'; }
    item.addEventListener('mouseenter', show);
    item.addEventListener('mouseleave', hide);
    item.addEventListener('focusin', show);
    item.addEventListener('focusout', function(e) { if (!item.contains(e.relatedTarget)) hide(); });
    item.addEventListener('keydown', function(e) { if (e.key === 'Escape') hide(); });
  });
});
