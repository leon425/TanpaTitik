let buttonLetter = document.getElementsByClassName('buttonLetter');

let buttonLetterMaxStock = document.getElementsByClassName('buttonLetterMaxStock');

for (let i = 0; i<buttonLetterMaxStock.length; i++) {
    buttonLetterMaxStock[i].addEventListener('click', function() {
    let itemId = this.dataset.item;  
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            console.log('max stock')
            document.getElementById(itemId+"_maxStock").style.display = 'block';
        }
    })

}

for (let i = 0; i<buttonLetter.length; i++) {
    buttonLetter[i].addEventListener('click', function() {
        let itemId = this.dataset.item; //this = self. It's the item we click on
        let sideAction = this.dataset.sideaction;
        console.log(itemId, sideAction);
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            updateCartQuantity(itemId,sideAction);
        }
    })

}

function updateCartQuantity(itemId,sideAction) {
    // console.log("User is logged in");
    // console.log(action)
    let url = '/updateCartQuantity/'; //the url we want to send our POST request

    
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type':'application/json', //the procedure
            'X-CSRFToken':csrftoken, // Setting the token you created in home.html
        },
        body: JSON.stringify({'itemId':itemId, 'sideAction':sideAction}) //The data we are going to send // We need to send a string type data. Not an object
     })

    .then((response) => { //promise
        return response.json(); //change the value to json data
    })
    .then((data) => { //promise
        console.log(data);
        const myTimeout = setTimeout(() => {location.reload()}, 200);
    })
    .catch((message) => {
        console.log(message);
    })


}

// REMOVE FROM CART & WISHLIST
let closeItem = document.getElementsByClassName('removeItem');

for (let i = 0; i<closeItem.length; i++) {
    closeItem[i].addEventListener('click', function() {
    let productId = this.dataset.productid;  
    let action = this.dataset.action
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            removeFromCartWishlist(productId,action);
        }
    })

}

function removeFromCartWishlist(productId,action) {
    let url = '/removeFromCartWishlist/'; //the url we want to send our POST request

    
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type':'application/json', //the procedure
            'X-CSRFToken':csrftoken, // Setting the token you created in home.html
        },
        body: JSON.stringify({'productId':productId, 'action':action}) //The data we are going to send // We need to send a string type data. Not an object
     })

    .then((response) => { //promise
        return response.json(); //change the value to json data
    })
    .then((data) => { //promise
        console.log(data);
        const myTimeout = setTimeout(() => {location.reload()}, 200);
    })
    .catch((message) => {
        console.log(message);
    })


}