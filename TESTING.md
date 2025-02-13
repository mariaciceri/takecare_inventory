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
| ordering/test/test_urls.py | ![PEP8 for ordering/test/test_urls.py ](/docs/images/pep8-testurls-ordering.png) | no issues |
| ordering/urls.py | ![PEP8 for ordering/urls.py ](/docs/images/pep8-urls-ordering.png) | no issues |
| ordering/views.py | ![PEP8 for ordering/views.py ](/docs/images/pep8-views-ordering.png) | no issues |
| ordering/test/test_views.py | ![PEP8 for ordering/test/test_views.py ](/docs/images/pep8-testviews-ordering.png) | no issues |
| home/apps.py | ![PEP8 for home/apps.py ](/docs/images/pep8-apps-home.png) | no issues |
| home/urls.py | ![PEP8 for home/urls.py ](/docs/images/pep8-urls-home.png) | no issues |
| home/views.py | ![PEP8 for home/views.py ](/docs/images/pep8-views-home.png) | no issues |
| inventory/urls.py | ![PEP8 for home/views.py ](/docs/images/pep8-urls-inventory.png) | no issues |
| inventory/settings.py | ![PEP8 for home/views.py ](/docs/images/pep8-settings.png) | no issues |

### Compatibility

+ The page was tested for compatibility on Firefox, Chrome, and Safari, and it functions flawlessly across all three browsers.

    + Firefox:
    ![Page working on firefox gif](/docs/images/firefox.gif)

    + Chrome:
    ![Page working on chrome gif](/docs/images/chrome.gif)

    + Safari:
    ![Page working on safari gif](/docs/images/safari.gif)

### Responsiveness

+ The page is responsive and works well for both small and large screens.

![Page responsiveness gif](/docs/images/responsiveness.gif)

### Manual Testing

### Automated testing

### Bugs

| Bug | Fix |
| --- | --- |