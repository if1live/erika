$(function() {
    var availableTerms = [
		{% for filetype in filetype_list %}"{{ filetype }}",
		{% endfor %}
    ];
    $( ".filetype_autocomplete" ).autocomplete({
        source: availableTerms
    });
});

