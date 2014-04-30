$(function() {
    setInterval(load_more, 3000);
    $('.btnReply').click(reply_tweet);

    $('#btnPost').click(post_tweet);
});

function load_more() {
    timestamp_now = $('#timestamp_now').val()
    $.post("/t/load_more_tweets/", {
        timestamp_now: timestamp_now,
    }, function(data) {
        if (data['success']) {
            add_tweet(data['html'], true);
            $('#timestamp_now').val(data['timestamp_now'])
        };
    });
}

function post_tweet(event) {
    $('#btnPost').attr("disabled", "disabled")
    $('#btnPostText').text("Posting")
    $.post("/t/post_tweet/", {
        content: $('#content_input').val(),
    }, function(data) {
        if (data['success']) {
            html = data['html']
            add_tweet(html, true)
            $('.btnReply').click(reply_tweet);
        }
        $('#content_input').val("")
        $('#btnPost').removeAttr("disabled")
        $('#btnPostText').text("Post")
    });
}

function reply_tweet(event) {
    tweet_pk = $(this).attr('tweet_pk')
    reply_content = $(this).prev().val()
    $(this).attr("disabled", "disabled")
    $.post("/t/reply/", {
        tweet_pk: tweet_pk,
        reply_content: reply_content,
    }, function(data) {
        if (data['success']) {
            html = data['html']
            tweet_pk = data['tweet_pk']
            add_reply(tweet_pk, html, true)
        }
        get_reply_btn(tweet_pk).removeAttr("disabled")
        get_reply_btn(tweet_pk).prev().val("")
    });
}

function add_tweet(html, animate) {
    if (animate) {
        $(html).prependTo($('#tweets_block')).hide().slideDown()
    } else {
        $(html).prependTo($('#tweets_block'))
    }
    $('#tweets_count').text(
        (parseInt($('#tweets_count').text()) + 1).toString()
    );
}

function add_reply(tweet_pk, html, animate) {
    if (animate) {
        $(html).appendTo(get_tweet(tweet_pk).find('.comments')).hide().fadeIn()
    } else {
        $(html).appendTo(get_tweet(tweet_pk).find('.comments'))
    }
}

function get_tweet(tweet_pk) {
    return $('.post[tweet_pk=' + tweet_pk + ']')
}

function get_reply_btn(tweet_pk) {
    return $('.btnReply[tweet_pk=' + tweet_pk + ']')
}