# Project Mgr

Placeholder; not in use.

## Think outside of the box
Think creatively about how to detail out features.

## Explain feature value
Provide a technical and business case explanation about feature value. Break down features and functionality in the following way. The following example would be for user login:
- User Login: As a user, I can log in to the application so that I can make changes. This prevents anonymous individuals from accessing the admin panel.
- Acceptance Criteria
    * On the login page, I can fill in my email address:
    * This field is required.
    * This field must enforce email format validation.
    * On the login page, I can fill in my password:
    * This field is required.
    * The input a user types into this field is hidden.
    * On failure to log in, I am provided an error dialog:
    * The error dialog should be the same if the email exists or not so that bad actors cannot glean info about active user accounts in our system.
    * Error dialog should be a red box pinned to the top of the page.
    * Error dialog can be dismissed.
    * After 4 failed login attempts, the form becomes locked:
    * Display a dialog to the user letting them know they can try again in 30 minutes.
    * Form stays locked for 30 minutes and the frontend will not accept further submissions.