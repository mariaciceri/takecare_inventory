$(document).ready(function () {

    // Populate with session items
    $.ajax({
        type: "GET",
        url: "session_items",
        success: function (response) {
            $("#item-list").empty();
            response.order_items.forEach(item => {
                $("#item-list").prepend(
                    `<li data-id="${item.item_id}">${item.name} - ${item.quantity}</li>
                        <button class="remove-item" data-action="remove/${item.item_id}">&times;</button>
                        `
                )
            });
        },
        error: function (error) {
            console.log('ERROR', error)
        }
    });

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
                );
                $("#item-list").empty();

                response.order_items.forEach(item => {
                    $("#item-list").prepend(
                        `<li data-id="${item.item_id}">${item.name} - ${item.quantity}</li>
                        <button class="remove-item" data-action="/order/remove/${item.item_id}">&times;</button>
                        `
                    )
                });
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