$(document).ready(function () {
    if (window.location.pathname === "/") {
        // Populate with session items
        $.ajax({
            type: "GET",
            url: "session_items",
            success: function (response) {
                $("#item-list").empty();
                response.order_items.forEach(item => {
                    $("#item-list").prepend(
                        `<li data-id="${item.item_id}">${item.name} - <input type="number" value="${item.quantity}"
                        min="1" class="item-quantity-adjust">
                        <button class="remove-item waves-effect waves-light btn-small" data-item_id="${item.item_id}">&times;</button>
                        </li>
                        `
                    )
                });
            },
            error: function (error) {
                console.log('ERROR', error)
            }
        });
    };

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
                        `<li data-id="${item.item_id}">${item.name} - <input type="number" value="${item.quantity}"
                        min="1" class="item-quantity-adjust">
                        <button class="remove-item waves-effect waves-light btn-small" data-item_id="${item.item_id}">&times;</button>
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

        // TODO : make it a nice transition
        if (quantity < 1) {
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
        }

        //TO DO fix the console.logs
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
                );
                $("#item-list").empty();
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

    // Display items in past orders
    $("a[data-id]").on("click", function (e) {
        e.preventDefault();

        let orderId = $(this).data("id");

        $.ajax({
            type: "GET",
            url: `/orders/order${orderId}`,
            success: function (response) {
                $("#order-details").empty();
                response.order_items.forEach(function (item) {
                    $("#order-details").prepend(
                        `<li>${item.name} - ${item.quantity}</li>`
                    )
                });

                const isDisabled = response.status !== 0;
                $("#order-details").append(
                    `<button type="button" class="edit-order ${isDisabled ? 'btn-flat disabled' : 'waves-effect waves-light btn-small'}" data-id="${orderId}">
                            Edit Order
                        </button>`
                );
            },
            error: function (error) {
                console.log('Error fetching order items:', error);
                $("#order-details").html("<p>Failed to load order items.</p>");
            }
        });
    });

    // Edit order
    $("#order-details").on("click", ".edit-order", function (e) {
        e.preventDefault();

        const orderId = $("a[data-id]").data("id");

        $.ajax({
            type: "GET",
            url: `/edit_order/${orderId}`,
            success: function (response) {
                window.location.href = "/";
            },
            error: function (error) {
                console.log('Error editing order:', error);
            }
        });
    });

    // Filter items by category
    $("#category").change(function () {
        const category = $(this).val();

        $.ajax({
            type: "GET",
            url: `/filter_items/${category}`,
            success: function (response) {
                const items = response.items;
                const itemSelect = $('#item');
                itemSelect.empty();

                // Add new options
                items.forEach(function (item) {
                    itemSelect.append(new Option(item.name, item.id));
                });

                $('select').formSelect();
            },
            error: function (error) {
                console.log('Error fetching items:', error);
            }
        });
    });

    // Materialize CSS
    $('.sidenav').sidenav();

    $('select').formSelect();
});
