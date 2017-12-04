// Code from https://github.com/kimmobrunfeldt/progressbar.js/blob/gh-pages/examples/password-strength/main.js
var weakColor = [252, 91, 63];  // Red
var strongColor = [111, 213, 127];  // Green

// Interpolate value between two colors.
// value: 0 means color A, 0.5 is halfway between, and 1 means color B
function interpolateColor(rgbA, rgbB, value) {
    var rDiff = rgbA[0] - rgbB[0];
    var gDiff = rgbA[1] - rgbB[1];
    var bDiff = rgbA[2] - rgbB[2];
    value = 1 - value;
    return [rgbB[0] + rDiff * value, rgbB[1] + gDiff * value, rgbB[2] + bDiff * value];
}

function rgbToString(rgb) {
    return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
}

function barColor(progress) {
    return rgbToString(interpolateColor(weakColor, strongColor, progress));
}

function onLoad() {
    // TODO convert to jQuery
    document.querySelectorAll('.progress').forEach(function (element) {
        // In [0,1]; how much of the hour target was completed
        var complete = Math.min(1, element.dataset.proportion.toLocaleString('en-US').toFractional(2));

        var bar = new ProgressBar.Line(element, {
            from: {color: barColor(0)},       // red
            to: {color: barColor(complete)},  // green
            duration: 1400,
            easing: 'easeOut',
            strokeWidth: 5,
            step: function (state, bar) {
                bar.path.setAttribute('stroke', state.color);
                bar.setText(element.dataset.name + ' (target: ' + element.dataset.target + ' hours)');
            }
        });
        bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
        bar.text.style.fontSize = '1.5rem';

        bar.animate(complete);
    });
}

window.onload = onLoad;