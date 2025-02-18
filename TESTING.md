# TESTING

+ All the tests performed on the page are registered here.

## Code Validation

### HTML/CSS validation

+ The page was run through [HTML W3C Validator](https://validator.w3.org) and [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator). 

| Page | Validator | Screenshot | Notes |
| --- | --- | --- | --- |
| Home | HTML | ![HTML validator for home page](/docs/images/html-validator-home.png) | Google validator provides the meta like this |
| Login | HTML | ![HTML validator for login page](/docs/images/html-validator-login.png) | no warnings |
| Ordering page | HTML | ![HTML validator for ordering page page](/docs/images/html-validator-ordering.png) | Google validator provides the meta like this. Warning for empty header is because it is added dinamically |
| Orders page | HTML | ![HTML validator for orders page page](/docs/images/html-validator-orders.png) | Google validator provides the meta like this |
| Sign out | HTML | ![HTML validator for sign out page](/docs/images/html-validator-signout.png) | no warnings |
| Sign up | HTML | ![HTML validator for sign up page](/docs/images/html-validator-signup.png) | no warnings |
| Unauthorized view | HTML | ![HTML validator for unauthorized view page](/docs/images/html-validator-unauthorized.png) | Google validator provides the meta like this |
| Multiple pages | CSS | ![CSS validator for all CSS files](/docs/images/css-validator-all-pages.png) | no warnings/errors |


### Lighthouse

+ Lighthouse in DevTools confirms that the overall performance is efficient, accessibility standards are met, and the chosen colors and fonts ensure readability.

    + Home page
    ![Lighthouse performance screenshot](/docs/images/lighthouse-home.png)

    + Ordering page
    ![Lighthouse performance screenshot](/docs/images/lighthouse-ordering.png)

    + Orders page
    ![Lighthouse performance screenshot](/docs/images/lighthouse-orders.png)

### PEP8 

+ All Python files were run through [PEP8 CI Python Linter](https://pep8ci.herokuapp.com).
+ Unchanged and/or unused files were excluded as they are expected to be valid.

| File | Screenshot | Notes |
| --- | --- | --- |
| ordering/admin.py | ![PEP8 for ordering/admin.py ](/docs/images/pep8-admin-ordering.png) | no issues |
| ordering/apps.py | ![PEP8 for ordering/apps.py ](/docs/images/pep8-apps-ordering.png) | no issues |
| ordering/templatetags/custom_filters.py | ![PEP8 for ordering/templatetags/custom_filters.py ](/docs/images/pep8-custom-ordering.png) | no issues |
| ordering/models.py | ![PEP8 for ordering/models.py ](/docs/images/pep8-models-ordering.png) | no issues |
| ordering/urls.py | ![PEP8 for ordering/urls.py ](/docs/images/pep8-urls-ordering.png) | no issues |
| ordering/views.py | ![PEP8 for ordering/views.py ](/docs/images/pep8-views-ordering.png) | no issues |
| home/apps.py | ![PEP8 for home/apps.py ](/docs/images/pep8-apps-home.png) | no issues |
| home/urls.py | ![PEP8 for home/urls.py ](/docs/images/pep8-urls-home.png) | no issues |
| home/views.py | ![PEP8 for home/views.py ](/docs/images/pep8-views-home.png) | no issues |
| inventory/urls.py | ![PEP8 for home/views.py ](/docs/images/pep8-urls-inventory.png) | no issues |
| inventory/settings.py | ![PEP8 for home/views.py ](/docs/images/pep8-settings.png) | no issues |
| test/test_admin.py | ![PEP8 for test/test_admin.py](/docs/images/pep8-test-admin.png) | no issues |
| test/test_urls.py | ![PEP8 for test/test_urls.py](/docs/images/pep8-test-urls.png) | no issues |
| test/test_views.py | ![PEP8 for test/test_views.py](/docs/images/pep8-test-views.png) | no issues |

## Compatibility

+ The page was tested for compatibility on Firefox, Chrome, and Safari, and it functions flawlessly across all three browsers.

    + Firefox:
    ![Page working on firefox gif](/docs/images/firefox.gif)

    + Chrome:
    ![Page working on chrome gif](/docs/images/chrome.gif)

    + Safari:
    ![Page working on safari gif](/docs/images/safari.gif)

## Responsiveness

+ The page is responsive and works well for both small and large screens.

![Page responsiveness gif](/docs/images/responsiveness.gif)

## Manual Testing

+ Manual testing was performed to ensure that the application behaves as expected in real-world usage. Each feature was tested by manually interacting with the interface, verifying functionality, and identifying any issues.

+ Users pages

| Page | Action | Result |
| --- | --- | --- |
| Home | Click on login button on navbar | Takes user to the page to login |
| Home | Click on register button on navbar | Takes user to sign up page |
| Home | Click on the email link in the contact section. | Opens the user's email provider with the page's email pre-filled in the recipient field |
| Home | Click on LinkedIn link in the contact section | Opens LinkedIn page on another tab |
| Sign in | Click on the sign up link | Takes the user to the sign up page |
| Sign in | Type wrong/non-existing username/password | Display a message informing the user of the problem |
| Login/Sign up | Click on the home link | Takes the user to the home page |
| Sign up | Click on the sign in link | Takes the user to the sign in page |
| Sign up | Types wrong/non-existing username/password | Displays a message informing the user of the problem |
| Sign up | Type an username that is already taken | Displays a message notifying the user that the selected username is already taken |
| Sign up | Type an email that is already taken | Displays a message notifying the user that the provided email is already associated with another user |
| Sign up | Type an invalid password | Displays a message explaining why the chosen password does not meet the requirements |
| Unauthorized Page/Ordering/Orders | Click on logout button in the navbar | Takes user to the logout confirmation page |
| Ordering | Click on the 'x' button to close informational message | Hides the message and change the button to an arrow down |
| Ordering | Click on the arrow down to display informational message | Shows the message and change the button to a 'x' |
| Ordering | Click on the category select field | Show available categories |
| Ordering | Select one of the categories | Filter the items by category |
| Ordering | Click on the item select field | Show available items |
| Ordering | Click on the add button without selecting quantity | Shows a 1.5-second notification that the quantity must be a positive integer |
| Ordering | Click on the add button with item quantity greater than the available in stock | Shows a 1.5-second notification of the available stock quantity |
| Ordering | Click the add button for an item already in the order | Increase the quantity of the item in the order by the amount selected |
| Ordering | Click the add button for an item already in the order when the total quantity exceeds stock availability.| Shows a 1.5-second notification of the available stock quantity |
| Ordering | Click on the add button with item quantity less or equal than the available in stock | Shows a 1.5-second notification that the item was added, then displays the item, its quantity, and a 'remove' button below the form |
| Ordering | Click on the 'remove' button of an item | Shows a 1.5-second notification that the item was removed and removes the item from the page |
| Ordering | Click on the save button without any items | Shows a 1.5-second notification that there are no items to order |
| Ordering | Click on the save button with at least one item | Shows a 1.5-second notification that the order was saved |
| Ordering | Click on the orders button on the navbar | Takes the user to the past orders page |
| Orders | Click on the home button on the navbar | Takes the user to the main (ordering) page |
| Orders | Click on an order | Displays the items and its quantities for that order below it. If the order is pending, displays edit and delete button |
| Orders | Click on the edit button | Redirects to the main page with the order items and a message indicating the order being edited |
| Orders | Click on the delete button | Opens a modal to confirm deletion |
| Orders | Click on the yes button | Deletes the order and erases from the page |
| Orders | Click on the no button | Closes the modal |
| Sign out | Click sign out button | Confirms signing out and takes user to the landing page |
| All pages | Click on LinkedIn link in the footer section | Opens LinkedIn page on another tab |

+ Admin page

| Page | Action | Result |
| --- | --- | --- |
| Admin home page | Click on "Categorys" button | Takes the user to the categories page |
| Category page | Click on "Add Category" button | Takes the user to the adding category page with name and description fields | 
| Add Category page | Click on "Save" button with name field filled | Saves the category and takes the user back to the Add Category page and displays a message confirming addition | 
| Add Category page | Click on "Save and add another" button with name field filled | Saves the category, erases fields and displays a message confirming addition | 
| Add Category page | Click on "Save and continue editing" button with name field filled | Saves the category, displays confirmation message and adds a delete button |
| Add Category page | Click on any button without the name field filled | Displays a message that the name field must be filled |
| Categorys/Items/Orders/Users page | Select entries and select "Delete selected --entries--" on actions dropdown | Asks for confirmation before deleting |
| Delete confirmation page | Click on "Yes, I'm sure" button | Deletes entry and take back to all entries page |
| Delete confirmation page | Click on "No, take me back" button | Takes the user back to all entries page |
| A Category/Item/Order/User page | Click on "Delete" button | Asks for confirmation before deleting |
| Admin home page | Click on "Items" button | Takes the user to the items page |
| Items page | Click on "Add item" button | Opens the add item page with the name field, category dropdown, expiration date picker, is critical checkbox and quantity in stock number input |
| Items/Orders page | Clicks on any of the filters | Filters the items/orders displayed on the screen |
| Add item page | Click on any of the save buttons without name, category, expiration date or quantity in stock input | Displays a message and marks the fields that must be filled in red |
| Add item page | Click on any save button with already taken name | Displays a message and marks the name field in red with a informative message |
| Admin home page | Click on "Orders" button | Takes the user to the orders page |
| Orders page | Select orders and "Approve orders"/"Reject orders" in actions dropdown | If all orders can be approved/rejected, display a confirmation message, otherwise display a message with which orders couldn't be processed and why |
| Admin home page | Click on "Users" button | Takes the user to the users page |
| Users page | Clicks on an user | Displays all the django built-up functionalities and a "is approved" checkbox.

## Automated testing

## Bugs

| Bug | Fix |
| --- | --- |
| Adding the same item to the order created duplicate entries instead of increasing the quantity | When adding an item to the order, go through the session and if the item is already present, increase the quantity |
| Updating the item quantity to over the max available was not updating it in the session | Going through the session to update it with the max quantity |
| General home page was not loading properly for authenticated users | Checked which was the requested path and show the proper content |
| If after clicking edit, going back to the orders page and deleting the order, its content remained available for editing | Clear the session after deleting the order and verify if it's empty to remove localStorage data |
| Alert messages were displaying in the admin login page | Remove the message block from the base.html and place it in the index.html | // RE DO
| 