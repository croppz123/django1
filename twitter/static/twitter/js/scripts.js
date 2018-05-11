
function vote(element, callback_url) {
    $.ajax(callback_url, {
        success: function(data) {
            if (data['direction'] == 1) {
                $(element).closest('div').find('#score').removeClass("badge-danger badge-dark")
                $(element).closest('div').find('#score').addClass("badge-success")
            } else if (data['direction'] == -1) {
                $(element).closest('div').find('#score').removeClass("badge-success badge-dark")
                $(element).closest('div').find('#score').addClass("badge-danger")
            } else {
                $(element).closest('div').find('#score').removeClass("badge-success badge-danger")
                $(element).closest('div').find('#score').addClass("badge-dark")
            }

            var updated_score = data['updated_score']
            if (updated_score > 0) {
                updated_score = '+' + updated_score
            }
            $(element).closest('div').find('#score').text(updated_score);
        }
    });
}

function delete_tweet(element, callback_url, in_detailed_view) {
    $.ajax(callback_url, {
        success: function(data) {
            if (window.confirm("Are you sure?")) {
                if (in_detailed_view) {
                    window.location.replace("/twitter");
                } else {
                    $(element).closest('div.row').remove();
                }
            }
        }
    });
}
