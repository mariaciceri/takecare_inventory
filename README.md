# TakeCare Inventory Management

[TakeCare Inventory Management](https://takecare-inventory-187635d57664.herokuapp.com/) is a web application designed for healthcare professionals to manage stock levels and request products efficiently.

- User Access
    - Users must log in to access the platform.
    - New users require approval; upon registration, a request is sent to the admin panel for manager approval.
- Ordering Process
    - Approved users can search for items, filter them by category, add them to an order list, and submit requests.
    - Orders require approval; while pending, users can modify them.
- Manager Role
    - Managers can approve or reject orders but cannot modify them.
    - They are responsible for updating item categories, stock quantities, expiration dates, and marking critical products.

The page is also fully responsive, although the focus is to be used at a computer and not mobile.

## Features
### Admin panel
- When an admin logs in, an alert message is displayed if there are expired or near-expiry items, low-stock items, or pending user approvals.
- When approving multiple orders at once, if stock is insufficient for all, older orders will be approved first, while newer ones will stay pending. An alert message will indicate which orders couldn't be fulfilled due to low stock.
- Manager can not add items without expiration date and the expiration date must be in the future.
- When an order is approved, the items are subtracted from the stock.

### User page
- Approved users can filter items by category.
- Users cannot add a quantity greater than the available stock; a message will display the available amount.
- Users can edit item quantities in their session, up to the maximum available:
    - If the entered quantity exceeds stock, it is automatically adjusted to the maximum.
    - If the quantity is less than 1, the item is removed from the list.
- If the same item is added again via the form, the quantity updates. If the total exceeds available stock, the item is not added.
- When the order is submitted, the home page is cleaned and the user can start a new request. If they leave an unsent order, the items in the order won't be lost if the page is closed/reloaded.
- In the orders page, the users can see their past orders, items ordered, and statuses and modify the order if it is still pending.



- ERD for the project:
![erd](/docs/images/erd.png)


- Initial wireframes:

![Page without order](/docs/images/without-order.png)
![Login page](/docs/images/login.png)
![Page with order](/docs/images/with-order.png)
![Order page](/docs/images/orders-page.png)
![Approved order](/docs/images/approved-order.png)
![Pending order](/docs/images/pending-order.png)

## Technologies

+ [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) structures the page.
+ [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) defines the style and layout.
+ [Materialize](https://materializecss.com/) provides the overall styling framework.
+ [Git](https://git-scm.com/) manages version control.
+ [Github](https://github.com/) hosts the project.
+ [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) with [JQuery](https://jquery.com/) add interactivity to the page.
+ [Django](https://www.djangoproject.com/) connects the front-end and back-end.
+ [PostgresQL](https://www.postgresql.org/) (provided by Code Institute) stores data.
+ [Heroku](https://www.heroku.com/) handles deployment.

## Deployment
### Deployment to Heroku

+ Clone the repository from GitHub page by running the command `git clone https://github.com/mariaciceri/takecare_inventory.git`;
+ Save the project on your own GitHub account by using the command `git push`
+ Create a new Heroku app by clicking on "New" and then "Create new app" on their page;
![Heroku menu with new app creating menu](/docs/images/heroku-new-app.png)
+ In the Deploy tab, look for "Deployment method" and select GitHub;
![Heroku menu with deploy selected](/docs/images/heroku-deploy.png)
+ Connect to your GitHub account if not done already and right below it, find your repository and connect to Heroku;
![Heroku Deployment method and App connected to GitHub](/docs/images/heroku-github.png)
+ Give your app a unique name and set the region accordingly. Click create app.
+ In the Settings tab, set one Config Vars:
    + DATABASE_URL(key): -your own database of choice-(value)
    + SECRET_KEY (key): -choose an unique and strong password-(value)
![Heroku config vars](/docs/images/heroku-config-vars.png)
+ In the Deploy tab, scroll down to Manual Deploy, confirm that you are deploying from "main" and click on "Deploy Branch";
![Heroku Manual deploy](/docs/images/heroku-manual-deploy.png)
+ Alternatively, enable "Enable Automatic Deploys";
![Heroku Automatic deploy](/docs/images/heroku-automatic-deploy.png)
+ It may take a couple of minutes to deploy, after completed, a "View" button will be available and it will take you to the deployed page.

### Run locally

+ If Python ins't installed, download from the [official webpage](https://www.python.org/downloads/).
+ For this project to run with all its functionalities, install:
    + `pip install -r requirements.txt`
+ Clone the repository from GitHub page by running the command `git clone https://github.com/mariaciceri/takecare_inventory.git` 
+ Alternatively, download it as a ZIP file from `https://github.com/mariaciceri/takecare_inventory` and extract it to a chosen location in your computer;
+ In `settings.py`:
    + Set the `DEBUG` variable to `True` while developing to display error messages on the screen.
    + Uncomment the `DATABASES` variable and comment the one below it.
    + Set the `SECRET_KEY` to a strong password. 


## Testing

## Credits

https://www.pexels.com/
https://unsplash.com/
https://materializecss.com/
https://icons8.com/icons