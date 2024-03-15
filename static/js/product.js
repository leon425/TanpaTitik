

let cartButton = document.getElementsByClassName('cartButton');
let wishlistButton = document.getElementsByClassName('wishlistButton');

// CART
for (let i = 0; i<cartButton.length; i++) {
    cartButton[i].addEventListener('click', function() {
        var productId = this.dataset.product; //this = self. It's the item we click on
        var actionCart = this.dataset.actioncart;
        console.log(productId, actionCart);
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            updateUserCart(productId, actionCart);
        }
    })

}

// WISHLIST
for (let i = 0; i<wishlistButton.length; i++) {
  wishlistButton[i].addEventListener('click', function() {
      var productId = this.dataset.product; //this = self. It's the item we click on
      var actionWishlist = this.dataset.actionwishlist;
      console.log(productId, actionWishlist);
      if(user === 'AnonymousUser') {
          console.log('User not logged in') //Code when the user isn't logged in
      } else {
          updateUserWishlist(productId, actionWishlist);
      }
  })

}


function updateUserCart(productId, action) {
    // console.log("User is logged in");
    // console.log(action)
    let url = '/updateCart/'; //the url we want to send our POST request

    
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
        const myTimeout = setTimeout(() => {location.reload()}, 100);
    })
    .catch((message) => {
        console.log(message);
    })


}

function updateUserWishlist(productId, action) {
  // console.log("User is logged in");
  // console.log(action)
  let url = '/updateItem/'; //the url we want to send our POST request

  
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
      const myTimeout = setTimeout(() => {location.reload()}, 100);
  })
  .catch((message) => {
      console.log(message);
  })
}



