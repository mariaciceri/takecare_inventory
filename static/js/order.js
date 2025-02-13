/**
* Display items in the ordering page
*/
function renderItems(items) {
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
                        <button class="remove-item btn-small blue-grey tooltipped" data-item_id="${item.item_id}" data-tooltip="Delete this item from order">
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

/**
* Display feedback to users after an action
*/
function messageDisplay(message) {
    $("#message").fadeOut("fast", function () {
        $(this).html(message).fadeIn("slow");
    });

    setTimeout(() => {
        $("#message").fadeOut("slow", function () {
            $(this).empty();
        })
    }, 1500);
}

$(document).ready(function () {
    if (window.location.pathname === "/") {
        // Populate with items in session
        $.ajax({
            type: "GET",
            url: "session_items",
            success: function (response) {
                if (response.order_items.length === 0) {
                    localStorage.removeItem("editingOrderId");
                }
                // Check if user is editing an order and display message
                if (localStorage.getItem("editingOrderId")) {
                    id = localStorage.getItem("editingOrderId");
                    $("#editing-message").text(`You are editing order ${id}.`);
                }
                
                renderItems(response.order_items);
            },
            error: function (error) {
                messageDisplay("Failed to load items. Please try again.");
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
                $("#item-quantity").val("");
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
        const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        // Deletes the item if user manually sets quantity to 0 or less
        if (quantity < 1) {
            $.ajax({
                type: "POST",
                url: `/delete_item/${itemId}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    messageDisplay(response.success);
                    $(`li[data-id="${itemId}"]`).remove();
                },
                error: function (error) {
                    messageDisplay(error.responseJSON.message);
                },
            });
            return;
        };

        $.ajax({
            type: "POST",
            url:`/update_item_quantity/${itemId}`,
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {
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
    $(".submit-order").on("click", function (e) {
        e.preventDefault();

        const form = $("#order-form");
        const formAction = form.attr("action");
        const orderId = localStorage.getItem("editingOrderId");

        const formData = form.serializeArray();

        if (orderId) {
            formData.push({ name: "order_id", value: orderId });
        }

        $.ajax({
            type: "POST",
            url: formAction,
            data: $.param(formData),
            success: function (response) {
                messageDisplay(response.success);
                $(".item-list-title").text("No items in cart");
                $("#item-list").empty();
                $("#editing-message").text("");

                localStorage.removeItem("editingOrderId");
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
        let orderDetails = $(this).closest("li").find(".order-details");

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

                const isProcessed = response.status !== 0;
                // Add undo and edit button
                orderDetails.append(
                    `
                    <button type="button" class="edit-order 
                    ${isProcessed ? 'hidden-button' : 'waves-effect waves-light btn-small blue-grey'} tooltipped"
                    data-id="${orderId}" data-tooltip="Edit your order.">
                            Edit<i class="material-icons right">edit</i>
                    </button>
                    <button type="button" class="delete-order 
                    ${isProcessed ? 'hidden-button' : 'btn modal-trigger waves-effect waves-light btn-small blue-grey'} tooltipped"
                    data-id="${orderId}" data-tooltip="Delete your order" data-target="modal1">
                        Delete<i class="material-icons right">clear</i>
                    </button>
                    `
                );

                // Initialize tooltips for newly added items buttons
                $('.tooltipped').tooltip({
                    enterDelay: 1000,
                    margin: 0,
                });
                orderDetails.slideToggle();
            },
            error: function (error) {
                orderDetails.html("<p>Failed to load order items.</p>");
            }
        });
    });

    //Edit order
    $(document).on("click", ".edit-order", function (e) {
        e.preventDefault();

        const orderId = $(this).data("id");
        localStorage.setItem("editingOrderId", orderId);

        $.ajax({
            type: "GET",
            url: `/edit_order/${orderId}`,
            success: function (response) {
                window.location.href = "/";
            },
            error: function (error) {
                $(".error-message").text("Failed to undo order. Please try again.");
            }
        });
    });
    
    // Delete order
    $(document).on("click", ".delete-order", function (e) {
        const orderId = $(this).data("id");

        $(".confirm-delete").data("id", orderId);
    });

    $(".confirm-delete").click(function (e) {
        e.preventDefault();

        const orderId = $(this).data("id");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        $.ajax({
            type: "POST",
            url: `/delete_order/${orderId}`,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                // Remove the order from the list
                $(`a[data-id="${orderId}"]`).closest("li").slideUp("slow", function () {
                    $(this).remove();
                });
            },
            error: function (error) {
                console.log(error.responseJSON.error);
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
                messageDisplay("Failed to filter items. Please try again.");
            }
        });
    });

    // Close/show information about how to use the app
    $(".close-form-text").click(function() {
        let isVisible = $(".information").is(":visible");
        
        $(".information").slideToggle( function () {
            if (isVisible) {
                $(".form-text").removeClass("form-text");
            } 
        });

        if (isVisible) {
            $(this).html("&#8744;");
        }
        else {
            $(this).html("&times;");
            $(".information").parent().addClass("form-text");
        }
    });

    // Materialize CSS initializators
    $('.sidenav').sidenav();

    $('select').formSelect();

    $('.tooltipped').tooltip({
        enterDelay: 1000,
        margin: 0,
    });

    $('.modal').modal();

    $('.parallax').parallax();
});
