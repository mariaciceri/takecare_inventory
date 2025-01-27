$(document).ready(function () {

    // Add item to cart
    $(".add-item").click(function (e) {
        e.preventDefault();

        const form = $("#order-form");
        const formAction = $(this).data("action");

        $.ajax({
            type: "POST",
            url: formAction,
            data: form.serialize(),
            success: function (response) {
                $("#message").html(
                    `<div class="success" role="alert">
                    ${response.success}
                    </div>`
                )
            },
            error: function (error) {
                $("#message").html(
                    `<div class="error" role="alert">
                    ${error.responseJSON.message}
                    </div>`
                )
            }
        });
    });
    // Remove item from cart

    // Update item quantity in cart

    // Place an order
    $("#order-form").submit(function (e) {
        e.preventDefault();

        const form = $(this);
        const formAction = form.attr("action");

        $.ajax({
            type: "POST",
            url: formAction,
            data: form.serialize(),
            success: function (response) {
                $("#message").html(
                    `<div class="success" role="alert">
                    ${response.success}
                    </div>`
                )
            },
            error: function (error) {
                $("#message").html(
                    `<div class="error" role="alert">
                    ${error.responseJSON.error}
                    </div>`
                )
            }
        })
    });
});