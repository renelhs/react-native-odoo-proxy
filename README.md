# React Native Odoo Proxy
Proxy between React Native and Odoo RPC.

This proxy acts as intermediary from React Native (or any other client) api call to Odoo. 
Since Odoo (v8.0 tested) uses JSON-RPC based communicating and not much libraries handle this, 
born the need of create React Native Odoo Proxy. 

## How its work

React Native Odoo Proxy is basically a bridge between any client (React Native tested) api call and Odoo API. 
Is created using Flask framework and OdooRPC library. There are two main functions:

#### login()

It takes care, as the name indicates, of any login request to Odoo, in case that your web client needs to login against 
Odoo, this is the way. You need to pass a JSON POST call with args: 'host', 'port', 'database', 'username', 'password'. 
Then you will get a http response from the proxy.


###### Access: your-url.com/api/login/

#### call_kw()

It's handle all methods calls. Like the login() you need to send the args: 'host', 'port', 'database', 'username', 'password',
however there is three more argument: 'model', 'method', 'options', this last is a dictionary where you can pass any data
to Odoo.

###### Access: your-url.com/api/call_kw/

### Example in React Native:

```
fetch(url, {
    method: 'POST',
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        host: '127.0.0.1',
        port: 8069,
        database: 'my_database',
        username: 'admin',
        password: 'password',
        model: 'my.odoo.model',
        method: 'my_odoo_method',
        options: {
            some_string: "I need this string in the Odoo method.",
        },
    }),
})
.then(response => response.json())
.then(responseJson => {
    console.log(responseJson);
})
.catch(error => {
    console.log(error);
});
```

### Check if the app is working

After you run the Flask server:
###### Access app in http://0.0.0.0:8080 you would see "Proxy Server Works!"
Error connecting to Odoo server:
###### In case of fail connection, additionally to the previous message you would see another so you can check de configuration or the server you are trying to reach.  
