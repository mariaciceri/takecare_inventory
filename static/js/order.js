$(document).ready(function () {

    function renderItems(items) {
        /**
        * Display items in the home page
        */
        if (items.length === 0) {
            $(".item-list-title").text("No items in cart");
            return;
        }
        else {
            $(".item-list-title").text("Items in cart");
        }
        $("#item-list").empty();
        items.forEach(item => {
            $("#item-list").prepend(
                `<li data-id="${item.item_id}">${item.name} 
                        <input type="number" value="${item.quantity}"
                        min="1" class="item-quantity-adjust">
                        <button class="remove-item waves-effect waves-light btn-small blue-grey tooltipped" data-item_id="${item.item_id}" data-tooltip="Delete this item from order">
                            &times;
                        </button>
                        </li>
                        `
            )
        });
        // Initialize tooltips for newly added items delete button
        $('.tooltipped').tooltip({
            enterDelay: 1000,
            margin: 0,
        });
    }

    function messageDisplay(message) {
        /**
        * Display feedback to users after an action
        */
        $("#message").fadeOut("fast", function () {
            $(this).html(message).fadeIn("slow");
        });

        setTimeout(() => {
            $("#message").fadeOut("slow", function () {
                $(this).empty();
            })
        }, 1500);
    }

    if (window.location.pathname === "/") {
        // Populate with items in session
        $.ajax({
            type: "GET",
            url: "session_items",
            success: function (response) {
                renderItems(response.order_items);
            },
            error: function (error) {
                console.log('ERROR', error)
            }
        });
    };

    // Add item to session
    $(".add-item").click(function (e) {
        e.preventDefault();

        const form = $("#order-form");
        const formAction = $(this).data("action");

        $.ajax({
            type: "POST",
            url: formAction,
            data: form.serialize(),
            success: function (response) {
                messageDisplay(response.success);
                renderItems(response.order_items);
            },
            error: function (error) {
                messageDisplay(error.responseJSON.message);
            }
        });
    });

    // Remove item from session and page
    $("#item-list").on("click", ".remove-item", function (e) {
        e.preventDefault();

        let itemId = $(this).attr("data-item_id");

        $.post(`/delete_item/${itemId}`,
            {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            function (response) {
                if (response.success) {
                    messageDisplay(response.success);
                    $(`li[data-id="${itemId}"]`).slideUp("slow", function () {
                        $(this).remove();
                    });
                    if (response.order_items.length === 0) {
                        $(".item-list-title").text("No items in cart");
                    }
                }
            },
            "json"
        );
    });

    // Update item quantity
    $("#item-list").on("change", ".item-quantity-adjust", function (e) {
        e.preventDefault();

        let itemId = $(this).parent().attr("data-id");
        let quantity = $(this).val();

        // Deletes the item if user manually sets quantity to 0 or less
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
            );
        };

        $.ajax({
            type: "POST",
            url:`/update_item_quantity/${itemId}`,
            data: {
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                quantity: quantity,
            },
            success: function (response) {
                messageDisplay(response.success);
            },
            error: function (error) {
                messageDisplay(error.responseJSON.message);
                if (error.responseJSON.max_quantity) {
                    $(`li[data-id="${itemId}"] input`).val(error.responseJSON.max_quantity);
                }
            }
        });
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
                messageDisplay(response.success);
                $(".item-list-title").text("No items in cart");
                $("#item-list").empty();
            },
            error: function (error) {
                messageDisplay(error.responseJSON.error);
            }
        });
    });

    // Display items in past orders
    $("a[data-id]").on("click", function (e) {
        e.preventDefault();

        let orderId = $(this).data("id");
        let orderDetails = $(this).closest("li").find("#order-details");

        $.ajax({
            type: "GET",
            url: `/orders/order${orderId}`,
            success: function (response) {
                orderDetails.empty();
                response.order_items.forEach(function (item) {
                    orderDetails.prepend(
                        `<li>
                        <p>${item.name}</p>
                        <p class="item-quantity">${item.quantity}</p>
                        </li>`
                    );
                });
                orderDetails.prepend(
                    `<li>
                        <p><strong>Name</strong></p>
                        <p class="item-quantity"><strong>Quantity</strong></p>
                        </li><hr>`
                );

                const isDisabled = response.status !== 0;
                // Add undo and edit button
                orderDetails.append(
                    `<button type="button" class="edit-order 
                    ${isDisabled ? 'btn-flat disabled' : 'waves-effect waves-light btn-small blue-grey'} tooltipped"
                    data-id="${orderId}" data-tooltip="This will delete the order, allowing you to update it. You must resend it after.">
                            Undo and Edit Order
                    </button>`
                );

                // Initialize tooltips for newly added items buttons
                $('.tooltipped').tooltip({
                    enterDelay: 1000,
                    margin: 0,
                });
                orderDetails.slideToggle();
            },
            error: function (error) {
                console.log('Error fetching order items:', error);
                orderDetails.html("<p>Failed to load order items.</p>");
            }
        });
    });

    // Undo and Edit order
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

                // Add filtered options
                items.forEach(function (item) {
                    itemSelect.append(new Option(item.name, item.id));
                });

                // Initialize select dropdown
                $('select').formSelect();
            },
            error: function (error) {
                console.log('Error fetching items:', error);
            }
        });
    });

    // Materialize CSS initializators
    $('.sidenav').sidenav();

    $('select').formSelect();

    $('.tooltipped').tooltip({
        enterDelay: 1000,
        margin: 0,
    });

});
