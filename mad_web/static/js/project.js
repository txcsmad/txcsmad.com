/* Project specific Javascript goes here. */
main();

function main() {
    footerUpdate()
}

window.onresize = function(event) {
    footerUpdate()
};

function footerUpdate() {
    var footerHeight = document.getElementById("footer").clientHeight;
    var body = document.getElementsByTagName("body")[0];
    body.style.marginBottom = footerHeight + "px";
}
