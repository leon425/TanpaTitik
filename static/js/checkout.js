var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

// PAYMENT METHOD
let paymentMethod = document.getElementsByClassName('payment-method');


for (let i = 0; i<paymentMethod.length; i++) {
    paymentMethod[i].addEventListener('click', function() {
        let method = this.dataset.method; //this = self. It's the item we click on
        console.log(method);
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            setPaymentMethod(method);
        }
    })

}

function setPaymentMethod(paymentMethod) {
    // console.log("User is logged in");
    // console.log(action)
    let url = '/paymentMethod/'; //the url we want to send our POST request

    
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type':'application/json', //the procedure
            'X-CSRFToken':csrftoken, // Setting the token you created in home.html
        },
        body: JSON.stringify({'paymentMethod':paymentMethod}) //The data we are going to send // We need to send a string type data. Not an object
     })

    .then((response) => { //promise
        return response.json(); //change the value to json data
    })
    .then((data) => { //promise
        console.log("data from views.py:", data);
        const myTimeout = setTimeout(() => {location.reload()}, 200);
    })
    .catch((message) => {
        console.log(message);
    })

}

// CONFIRM ORDER
let confirm_order = document.getElementById('confirm_order');
console.log(confirm_order)

confirm_order.addEventListener('click', function() {
    let status = this.dataset.status;
    if(user === 'AnonymousUser') {
        console.log('User not logged in') //Code when the user isn't logged in
    } else {
        confirmOrder(status);
    }
})

function confirmOrder(status) {
    console.log(status)
    let url = '/confirmOrder/'; //the url we want to send our POST request

    
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type':'application/json', //the procedure
            'X-CSRFToken':csrftoken, // Setting the token you created in home.html
        },
        body: JSON.stringify({'status':status}) //The data we are going to send // We need to send a string type data. Not an object
     })

    .then((response) => { //promise
        return response.json(); //change the value to json data
    })
    .then((data) => { //promise
        console.log("data from views.py:", data);
        const myTimeout = setTimeout(() => {location.reload()}, 200);
    })
    .catch((message) => {
        console.log(message);
    })

}