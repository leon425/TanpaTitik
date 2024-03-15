if (document.getElementById('carouselExampleIndicators') != undefined) {
  //Bootstrap Carousel Circle Colour
  var myCarousel = new bootstrap.Carousel(document.getElementById('carouselExampleIndicators'));


  // Code to run after the carousel has completed sliding to a new item
  $('#carouselExampleIndicators').on('slid.bs.carousel', function () {
  // console.log('Carousel slid to a new item!');

  // Log the index of the active item
  var activeIndex = $('.carousel-item.active').index();

  //Retrieve the circle color from alt attribute
  var circle_color = $('.carousel-item.active img').attr('alt');

  const circle = document.querySelector(".circle");
  circle.style.backgroundColor = circle_color; //add animation. Speed up the animatin

  });
}

// Wishlist Button front-end
$(function() {
    $(".heart").on("click", function() {
      $(this).toggleClass("is-active");
    });
  });


// Wishlist send to back-end
let updateButtons = document.getElementsByClassName('update-cart');

for (let i = 0; i<updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function() {
        var productId = this.dataset.product; //this = self. It's the item we click on
        var action = this.dataset.action;
        console.log(productId, action);
        if(user === 'AnonymousUser') {
            console.log('User not logged in') //Code when the user isn't logged in
        } else {
            updateUserWishlist(productId, action);
        }
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
        const myTimeout = setTimeout(() => {location.reload()}, 500);
    })
    .catch((message) => {
        console.log(message);
    })
}






