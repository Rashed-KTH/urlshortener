(function ($, window, document, undefined) {
    $(document).ready(function () {
        $("#shortifyButton").removeAttr("disabled");
        $("#shortifyInput").removeAttr("disabled");

        $("#shortifyButton").click(function () {
            var value = $("#shortifyInput").val().trim();

            if (value === "") return false;

            $.ajax("?url=" + value)
                .done(function(data, textStatus) {
                    add_message_block(data);

                    $("#shortifyInput").val("")
                })

                .fail(function(data, textStatus, errorThrown) {
                    add_message_block({ status: "fail", message: "Request failed (" + textStatus + ")." });
                });
        })
    })

    function add_message_block(data) {
        var className = "";
        var message = "";

        if (data.status === "fail") {
            className = "shortifyError"
            message = data.message;
        } else {
            if (data.url.length > 50) {
                url = data.url.substring(0,47) + "...";
            } else {
                url = data.url;
            }

            className = "shortifySuccess"
            message = "<b>" + data.short_url + "</b>" +
                      "<br><br> now redirects to: <br><br>" +
                      "<b title='" + data.url + "'>" + url + "</b>"
        }

        $("#shortifyResponse").prepend(
            "<p class=" + className + " style='display: none;''>" + message + "</p>"
        ).find("." + className + ":first").slideDown(100);
    }
})(jQuery, this, this.document);