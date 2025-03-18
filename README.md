# Community Toolshed

This is the 4th milestone project for the CodeInstitute level 5 Web Application Development Course

The Community Toolshed Renting Application is a platform that allows users to subscribe and rent tools and party items on a daily basis. Subscribers pay an annual fee to gain access to a shared inventory of tools and reusable party supplies, promoting sustainability, affordability, and community resource sharing.

This project is potentially something that will be reworked into a live project used by the Handcross Hardware local store, where I currently help at.

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
- ✅ I receive reminders when my subscription is about to expire.
- ✅ I can renew my subscription before it expires.
- ✅ If my subscription is inactive, I cannot rent items.

## User Requirements

A full list of the user requirements can be seen in the [TESTING.md file](/TESTING.md) 

## Features

### Main App Features

### Django App Structure 

### Database Design 

## UI/UX

### Mockups 

### Pages

### Structure and Navigation 

### Accessibility 

### Defensive Design 

## Deployment

Deployment is done through Heruko

## How to Use

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

## Future Considerations

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

### Resources

- [Pexels](https://www.pexels.com/) used for royalty free images 
    - home page image by ClickerHappy: https://www.pexels.com/photo/lawn-mower-vehicle-on-grass-589/
- the [code institute walkthrough project](https://github.com/Code-Institute-Solutions/boutique_ado_v1_sourcecode/tree/main/) was used as a starting point for this project
and the tutorial lessons where followed in order to create this project 
- [strip docs](https://docs.stripe.com/)
- [css.glass](https://css.glass) - for glassmorphism effect