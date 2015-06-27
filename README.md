# HeroDemo

This is a simple app to get you started using the UP API. This app will:

1.  Establish an OAuth connection
2.  Read the connected user's info from UP
3.  Create generic feed events in the UP app

To get started, [sign in](https://jawbone.com/up/developer/auth/login) to our [developer portal](https://jawbone.com/up/developer) (you can use your existing Jawbone UP account or create a new one).

Fill in the form to create your organization.

On your [organization page](https://jawbone.com/up/developer/account/), click Create App.

Fill in the form to create your application. If you are going to use the Heroku button to deploy this app, make sure you specify your URL domains in the form: `<app_name>.herokuapp.com`

Click the button below to deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

On the Heroku form, you will need to specify the following:

1.  **App Name/app_name** -  enter the same name in both fields and this should match the domain you specified when creating your UP app
2.  **client_id** - enter the Client Id from your UP app
3.  **app_secret** - enter the App Secret from your UP app
