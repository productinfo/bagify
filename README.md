CS50's Web Proggraming with Python and Javascript. Final Project

This project is an ecommerce site mockup.

The project's files consists of HTML and CSS files for the UI. (index.html, styles.css)
Javascript files for the frontend logic of each page.	
And the server side files (views.py, models.py, utils.py) which handle the backend logic.

The site's pages and their core purpose and functionality are:

	Index: 
		Serves as the main display of the brand, where the site's most popular and newest products are displayed aswell.

	Collections:
		Is the catalog of the website where all the products are displayed, the user is able to filter the catalog for better UE. 

	Product:
		The product page serves as a display page for each individual product, where the user can see more details of the product and add it to the cart

	Cart:
		Here is all the products the user added to his cart. 
		The cart is saved in the browser cookies, only the id of the product.
		When the user requests the page the server gathers more information (price, imageUrl, name) about each product and sends it back to the client.

	Checkout:
		Where the user can finish an purchase. 
		The page is contains a stepper which walk the user through the steps of finalizing the purchase, which are adding and address and then paying with paypal.
		The paypal button contained in the page will open a new tab in the paypal website where the payment will be handled and then the results will be posted back to the server with the address details the user had previously typed and then it will be handled by the server to see if it's all okay and nothing was tempered.

	Account Page:
		Contains users' information as well as options. The order history aswell as saved address are displayed and functionality (such as changing passwords, deleting the account, saving addresses) are displayed to the user.


