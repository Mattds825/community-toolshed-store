![community toolshed all devices](/documentation/all_devices_black.png)

# Community Toolshed

[live site](https://ci-community-toolshed-afafcfe7f3c4.herokuapp.com/)

This is the 4th milestone project for the CodeInstitute level 5 Web Application Development Course

The Community Toolshed Renting Application is a platform that allows users to subscribe and rent tools and party items on a daily basis. Subscribers pay an annual fee to gain access to a shared inventory of tools and reusable party supplies, promoting sustainability, affordability, and community resource sharing.

This project is potentially something that will be reworked into a live project used by the Handcross Hardware local store, where I currently help at.

## In a Nutshell

Community Toolshed is a full-stack e-commerce platform built with Django, Stripe, and Bootstrap, designed for a local hardware store’s rental service. The platform allows users to sign up, subscribe, and rent tools or party items, such as cutlery, plates, and power tools. Once subscribed, users can place rental orders, view past orders, and manage their profiles. Payments are securely processed using Stripe, ensuring a smooth checkout experience. The platform also includes a dedicated management system where store managers can add, edit, and remove products, as well as oversee rentals. A built-in maintenance system enables managers to track tool conditions, create repair tickets, and update tool statuses as needed. The site features a responsive, user-friendly interface, ensuring seamless navigation across devices.

This project was built using Code Institute’s Boutique Ado template as a foundation. However, significant modifications were made to the Django models, templates, and order logic to better suit the rental-based functionality and management features required for the Community Toolshed service. The project follows best practices in version control using Git and GitHub and is deployed on Heroku for live access.

## Project Goals

### 🔹 User & Subscription Management
Users can create an account and subscribe to access rentals.
Subscription is yearly ($10/year) and grants full access to item rentals.

### 🔹 Item Rentals (Tools & Party Items)
Tools: Individually tracked items with serial numbers, repair status, and availability.
Party Items: Bulk-tracked items (plates, cups, cutlery) with stock and damage tracking.
First-come, first-serve rental system.

### 🔹 Order & Rental Management
Users place rental orders for specific date ranges.
Orders track damaged items and cleaning requirements for reusable items.
Rentals must be returned before new orders are placed.

### 🔹 Payments & Transactions
Secure payment processing for subscriptions and rentals.
Payment statuses: pending, paid, failed.

### 🔹 Maintenance & Repairs
Tools marked as broken or needing repair are sent for maintenance.
Maintenance requests track repair status (pending, in_progress, fixed, written_off).

## 🎯 Business Objectives

This website should advertise the benefits of joining the Community Toolshed and subscribing to the rental service. The main goal is to attract new subscribers and encourage existing subscribers to continue their membership.

The business wants to be able to verify the identity of users and ensure that they are responsible renters. The business also wants to track the condition of items and ensure that they are maintained and repaired as needed.

There will be a 1 year subscription fee of £10 for all users. This fee will be used to maintain the website and cover the cost of repairs and maintenance.

## 📖 User Stories

### 1️⃣ As a Community Member, I want to rent tools so that I can complete home improvement projects affordably.

- ✅ I can browse available tools in the inventory.
- ✅ I can select a tool and choose a rental period.
- ✅ I can place an order for the tool (if available).
- ✅ I receive confirmation of my order.
- ✅ I can return the tool and report if it is broken or needs repair.

### 2️⃣ As a Party Host, I want to rent party items so that I don’t have to buy disposable supplies.

- ✅ I can browse available party items (plates, cups, cutlery, etc.).
- ✅ I can select a quantity of party items to rent.
- ✅ I can place an order for my event date.
- ✅ If items are broken or need cleaning, I can report them upon return.

### 3️⃣ As a Subscriber, I want to manage my membership so that I can continue renting items without interruption.

- ✅ I can subscribe and pay the $10 yearly fee.
- ✅ I can view my subscription status (active/inactive).
- ✅ If my subscription is inactive, I cannot rent items.

## User Requirements

A full list of the user requirements can be seen in the [TESTING.md file](/TESTING.md) 

## Features 

### Main App Features

#### User Authentication

- Users can sign up and login to the platform
- Users can logout of the platform

Users emails are unique and passwords are hashed for security

#### Browsing Items

- Users can browse all items available for rent
- Users can filter items by category
- Users can search for items by name

#### Item Details

- Users can view the details of an individual item
- Users can see the availability of an item
- Users can see the rental price of an item

#### Cart

Cart verifies if users are logged in and verified

- Users can add items to their cart
- Users can view their cart
- Users can remove items from their cart
- Users can adjust the quantity of items in their cart

#### Checkout

- Users can checkout their cart
- Users can pay for their cart
- Users can view their order confirmation

#### Orders

- Users can view their order history
- Users can view the details of an individual order

#### Maintenance

- Users can report an item as needing maintenance
- Managers can view all maintenance tickets
- Managers can update the status of a maintenance ticket
- Managers can create a new maintenance ticket

#### Profile

- Users can view their profile
- Users can update their profile
- Users can view their subscription status
- Users can renew their subscription
- Users can view their order history
- Users can request verification of their account

#### Subscription

- Users can subscribe to the platform
- Users can pay for their subscription
- Users can view their subscription status
- Users can renew their subscription

#### Stripe Integration

- Users can pay for their cart using stripe
- Users can pay for their subscription using stripe

#### Webhooks

- Webhooks are used to create redundancy in the payment system
- Webhooks are used to update the status of an order when a payment is successful
- Webhooks are used to send confirmation emails

### Django App Structure 

#### community_toolshed Main Project

here is where is main urls and the settings file lives

#### homepage App

here is the main landing page of the website, where users can see the main features of the website and sign up or login

#### profiles App

here is where the user profile is managed, users can update their profile, view their subscription status and renew their subscription, and see their order history and view their verification status

This app also contains the UserProfile Model

#### products App

Here is where the products are managed, users can view all items available for rent, view the details of an individual item, see the availability of an item and see the rental price of an item

This app contains the Item Model, the Category Model, the Tool Model and the PartyItem Model

This app also contains the views used by the manager to add and  edi items

#### cart App

Here is where the cart is managed, users can add items to their cart, view their cart, remove items from their cart and adjust the quantity of items in their cart

This app contains a cart contexts processor to ensure that the cart is available on all pages

#### checkout App 

Here is where the checkout process is managed, users can checkout their cart, pay for their cart and view their order confirmation

The subscription payment process is also managed here

This app contains the Order Model, the OrderItem Model and the Subscription Model

There is also a webhook handler to manage stripe webhooks and also to send confirmation emails

#### maintenance App  

here is where the maintenance process is managed, users can report an item as needing maintenance, managers can view all maintenance tickets, update the status of a maintenance ticket and create a new maintenance ticket

This app contains the MaintenanceTicket Model

### Database Design 

#### Item Model

![item model table](/documentation/erd/item_table.png)

- In the type field, the item is either a tool or a party item, 0 or 1 respectively
- In the current implementation the item can only have one category

#### Category Model

![category model table](/documentation/erd/category_table.png)

#### Tool Model

**Subclass of Item Model**

![tool model table](/documentation/erd/tool_table.png)

- The tool condition can be one fo the following
```python
TOOL_CONDITION = (
    (0, 'New'),
    (1, 'Fair'),
    (2, 'Poor'),
)
```
- The tool model has a serial number field to track individual tools. The item parent has and sku field which allows multiple tool of the same kind, and still be individually maintained

#### PartyItem Model

**Subclass of Item Model**

![party item model table](/documentation/erd/party_item_table.png)

- the party items are bulk tracked, so there is no serial number field, instead teh following fields are used to track the item
    - available_amount: the amount of items available for rent
    - broken_amount: the amount of items that are damaged
    - stock_amount: the amount of items in stock

#### Order Model

![order model table](/documentation/erd/order_table.png)

- The payment status can be one of the following
```python
PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
)
```
- the stripe_pid field is used to store the stripe payment id
- start_date and end_date are used to track the rental period
- the order is associated with a UserProfile for the user who placed the order, this allows the user to view their order history

#### OrderItem Model

![order item model table](/documentation/erd/order_item_table.png)

- the order item has a status, which can be:
```python 
ORDER_ITEM_STATUS = (
    ('reserved', 'Reserved'),
    ('active', 'Currently Rented'),    
    ('returned', 'Returned'),    
)
```
- the order item is associated with an order, this allows the user to view the details of an individual order
- the order item is directly associated with an item, this allows the user to view the details of an individual item

#### Subscription Model

![subscription model table](/documentation/erd/subscription_table.png)

- the subscription is associated with a UserProfile, this allows the user to view their subscription status
    - users with an active subscription can rent items
    - users with an inactive subscription cannot rent items
- the is a stripe_pid field to store the stripe payment id
- the subscription number is unique to each subscription and users can purchase a new subscription each year

#### UserProfile Model

![user profile model table](/documentation/erd/user_profile_table.png)

This model is used to store the user's profile information and is associated with the Django User model

- there is a verified field to track if the user has been verified
- there is a subscription field to track if the user has an active subscription
    - in practice this would allows managers to verify users once they visit the store

#### MaintenanceTicket Model

![maintenance ticket model table](/documentation/erd/maintenance_ticket_table.png)

A maintenance ticket is created when a user/manager reports an item as needing maintenance

- the status field can be one of the following
```python
MAINTENANCE_STATUS = (
    ('pending', 'Pending'),    
    ('fixed', 'Fixed'),
    ('written_off', 'Written Off'),
)
```
- the maintenance ticket is associated with an tool, this allows the user/manager to view the details of the tool and also view care instructions
- the maintenance ticket can be associated with an order, this allows the user/manager to track down the details of the order and also view the rental period and who rented the item

#### EmailAddress and EmailConfirmation Models

These are additional models that are used to manage the email verification process

![email address model table](/documentation/erd/email_address_table.png)
![email confirmation model table](/documentation/erd/email_confirmation_table.png)

#### Compete ERD

This is the complete ERD for the project

It was generated with the graph_models command and the image was created with GraphvizOnline



![complete erd](/documentation/erd/complete_erd.png)

## UI/UX

### Mockups 

No mockups were created for this project, it was designed as I went along based on the Code Institute walkthrough project.

The styling are mainly sticking to bootstrap defaults with some custom css for the glassmorphism effect and some others

### Pages

These are the main pages of the website, I will attach a screenshot of both the mobile and desktop view 

#### Sign In Page

#### Sign Up Page

#### Logout Page

#### Home Page

#### Products Page

#### Individual Item Page

#### Cart Page

#### Checkout (Payment) Page

#### Checkout (Success) Page

#### Checkout (Subscription Payment) Page

#### Checkout (Subscription Success) Page

#### Maintenance Page

#### Add Maintenance Ticket Page

#### Edit Maintenance Ticket Page

#### Complete(Open) Maintenance Ticket Page

#### Management Page

#### Add Tool Page

#### Edit Tool Page

### Structure and Navigation 

### Colors 

using default bootstrap colors to ensure consistency

### Accessibility 

Making sure to use bootstrap classes to ensure that the website is accessible

#### Hover on Buttons

All buttons have a hover effect to show that they are clickable

#### Focus on Inputs

All inputs have a focus effect to show that they are selected

#### Contrast

All text has a high contrast with the background to ensure readability

#### Confirmation, Information and Error Messages

- User receives a confirmation message when they have successfully completed an action
- User receives an error message when they have failed to complete an action
- User revives an information message when they need to know something

### Defensive Design 

- User has to be logged in to access certain pages
- User has to be verified to access certain pages
- User will be informed if they try to access a page they are not allowed to access

## Deployment

Deployment is done through Heruko

[live site](https://ci-community-toolshed-afafcfe7f3c4.herokuapp.com)

## How to Use

### As A User

1. Go to the website
2. Sign up for an account
3. confirm your email
4. fill out the detail in your profile
6. subscribe to the platform
7. activate your profile
8. browse the items available for rent
9. add items to your cart
10. checkout your cart
11. pay for your cart
12. view your order confirmation
13. open the order page to view your order details and change status (for testing purposes)

### As A Manager

**Test Superuser Account:**

- username: 
- password: 

1. Go to the website
2. Log into the superuser account
3. go to management page
4. add a new item
5. edit an item
6. view past orders
7. view specific order details and change status
8. go to maintenance page
9. add a new maintenance ticket
10. edit a maintenance ticket
11. view all maintenance tickets


### Stripe Card Test Numbers

You can use these card numbers at the checkout to test stripe payment integration

| CARD NUMBER |	SCENARIO | HOW TO TEST |
| --- | --- | ---|
| 4242424242424242 | The card payment succeeds and doesn’t require authentication. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 4000002500003155 | The card payment requires authentication. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 4000000000009995 | The card is declined with a decline code like insufficient_funds. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 6205500000000000004 |	The UnionPay card has a variable length of 13-19 digits. |	Fill out the credit card form using the credit card number with any expiration, CVC, and postal code.|

this information if from the stripe [docs](https://docs.stripe.com/payments/accept-a-payment?platform=web&ui=elements#enable-checkout-link)

## Testing

Testing information can be found in the [TESTING.md file](/TESTING.md)

## Future Considerations

Due to time constraints, there are some features that were not implemented in this project that could be added in the future

### Time Bound

- there is some redundancy in my tables that could be removed
- I managed to implement the maintenance system for tool, but did not have time to implement the cleaning system for the party items
- I waned to create dining sets with the part items but did not have time to implement this

### Future Features

- Add a feature to allow users to request items that are not currently in the inventory
- Flesh out the rating system to allow users to rate items and leave reviews
- use the built in stripe subscription feature to manage the subscription payments

## Credits 

### Technologies

- HTML/CSS/JS - Frontend and templates
- Bootstrap - CSS library
- Python, Django - Backend 
- PostgreSQL - Database
- Heroku - Hosting
- Git/Github - Version Control
- django SummerNote - styling django admin panel
- django crispy forms - for handling and creating forms
- [Dbdiagram.io](https://dbdiagram.io/d) - used to create database schema
- [stripe](https://stripe.com) - used to manage payments
- [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline)
- [AWS S3](https://aws.amazon.com/s3/) - used to store static files and media files

### Resources

- [Pexels](https://www.pexels.com/) used for royalty free images 
    - home page image by ClickerHappy: https://www.pexels.com/photo/lawn-mower-vehicle-on-grass-589/
- the [code institute walkthrough project](https://github.com/Code-Institute-Solutions/boutique_ado_v1_sourcecode/tree/main/) was used as a starting point for this project
and the tutorial lessons where followed in order to create this project 
- [stripe docs](https://docs.stripe.com/)
- [css.glass](https://css.glass) - for glassmorphism effect
- Youtube [tutorial by BugBytes](https://www.youtube.com/watch?v=qzrE7cfc_3Q&t=232s) for generating the ER diagrams for the django models