function createReplyAlert(target, bg, content, direction, adjust) {
    body = $(document.body);

    offset = target.offset();
    div = '<div></div>';

    replies = $(div).addClass("replies replies-absolute");
    
    container = $(div).appendTo(replies);
    container.addClass("bg-color-" + bg);
    container = $(div).appendTo(container);
    container.addClass("reply reply-text-only");
    
    $('<b></b>').appendTo(container).addClass("sticker sticker-color-" + bg + " sticker-" + direction);

    if (typeof content.auth != 'undefined') {
        $(div).appendTo(container).addClass('author').text(content.auth);
    }
    if (typeof content.date != 'undefined') {
        $(div).appendTo(container).addClass('date').text(content.date);
    }
    $(div).appendTo(container).addClass('text').text(content.text);

    if (typeof adjust.x == 'undefined') {
        adjust.x = 0;
    }
    if (typeof adjust.y == 'undefined') {
        adjust.y = 0;
    }
    replies.css("top", (offset.top + 10 + adjust.y) + "px");
    if (direction == "left") {
        replies.css("left", (offset.left + target.width() + 10 + adjust.x) + "px");
    } else if (direction == "right") {
        replies.css("left", (offset.left - 300 - 10 + adjust.x) + "px");
    } else {
        return;
    }

    replies.hide();
    body.append(replies);
    replies.click(function() {
       this_ = $(this);
       if (this_.queue('fx').length == 2) {
            this_.dequeue();
       } 
    }).fadeIn('fast').delay(30000).fadeOut('fast', function(){
        $(this).remove();
    });
    return replies;
}
