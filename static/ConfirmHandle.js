jQuery(document).ready(function() {

    jQuery('#confirm').on('click', function(event) {
        jQuery.ajax({
            data : {
                confirmData: 'go'
            },
            type : 'POST',
            url: '/confirm'
        })
        .done(function(data) {
            console.log("done");
        });
        event.preventDefault();
        alert("成功确认并提交");
    });
});
