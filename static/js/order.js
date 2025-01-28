$(document).ready(function () {
    // Populate with session items
    $.ajax({
        type: "GET",
        url: "session_items",
        success: function (response) {
            $("#item-list").empty();
            response.order_items.forEach(item => {
                $("#item-list").prepend(
                    `<li data-id="${item.item_id}">${item.name} - <input type="number" value="${item.quantity}" min="1" class="item-quantity-adjust">
                        <button class="remove-item" data-item_id="${item.item_id}">&times;</button>
                        </li>
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
                        `<li data-id="${item.item_id}">${item.name} - <input type="number" value="${item.quantity}" min="1" class="item-quantity-adjust">
                        <button class="remove-item" data-item_id="${item.item_id}">&times;</button>
                        </li>
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
    $("#item-list").on("click", ".remove-item", function (e) {
        e.preventDefault();

        let itemId = $(this).attr("data-item_id");

        $.post(`/delete_item/${itemId}`,
            {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            function (response) {
                if (response.success) {
                    $(`li[data-id="${itemId}"]`).remove();
                }
            },
            "json"
        )
    })

    // Update item quantity in cart
    $("#item-list").on("change", ".item-quantity-adjust", function (e) {
        e.preventDefault();

        let itemId = $(this).parent().attr("data-id");
        let quantity = $(this).val();

        $.post(`/update_item_quantity/${itemId}`,
            {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                quantity: quantity,
            },
            function (response) {
                if (response.success) {
                    console.log("YEAH BABE")
                }
                else {
                    console.log("NOPE")
                }
            },
            "json"
        )
    });

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