$('.js_like').on('click', function() {
    var $like = $(this);
    $.post("/like/", { type: "like", id: $like.data('id') })
        .done(function(resp) {
            $(this).parent().find('.js_cnt').text(resp.new_rating);
        });
});
