// Code from https://github.com/kimmobrunfeldt/progressbar.js/blob/gh-pages/examples/password-strength/main.js
function onLoad() {
    // TODO convert to jQuery
    document.querySelectorAll('.progress').forEach(function (element) {
        var bar = new ProgressBar.Line(element, {
            from: {color: 'rgb(252,91,63)'},  // red
            to: {color: 'rgb(111,213,127)'},  // green
            duration: 1000,
            easing: 'easeOut',
            strokeWidth: 5,
            step: function (state, bar) {
                bar.path.setAttribute('stroke', state.color);
            }
        });

        // In [0,1]; how much of the target hour goal was completed
        bar.animate(Math.min(1, element.dataset.info.replace(',', '.')));
    });
}

window.onload = onLoad;