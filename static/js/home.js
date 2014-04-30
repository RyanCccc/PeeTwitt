$(function() {
    $('#test_load_more').click(function(event) {
        $.post("/t/load_more_tweets/", {
            curr_pk: -1
        }, function(data) {
            console.log(data);
        });
    });

    $('#test_reply').click(function(event) {
        $.post("/t/reply/", {
            tweet_pk: 2,
            reply_content: 'Wo qu ni ma le ge B!!',
        }, function(data) {
            console.log(data);
        });
    });

    $('#test_post').click(function(event) {
        $.post("/t/post_tweet/", {
            content: 'My second post!!',
        }, function(data) {
            console.log(data);
        });
    });
});