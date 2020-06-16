var $ = jQuery.noConflict()

function abrirModal(url) {
    $('#info').load(url, function () {
        $(this).modal('show');
    });
}