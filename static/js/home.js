
if (document.getElementById('carouselExampleIndicators') != undefined) {
  //Bootstrap Carousel Circle Colour
  var myCarousel = new bootstrap.Carousel(document.getElementById('carouselExampleIndicators'));


  // Code to run after the carousel has completed sliding to a new item
  $('#carouselExampleIndicators').on('slid.bs.carousel', function () {
  // console.log('Carousel slid to a new item!');

  // Log the index of the active item
  var activeIndex = $('.carousel-item.active').index();
  // console.log('Active item index:', activeIndex);

  //Retrieve the circle color from alt attribute
  var circle_color = $('.carousel-item.active img').attr('alt');
  // console.log('Active item image source:', circle_color);

  const circle = document.querySelector(".circle");
  circle.style.backgroundColor = circle_color; //add animation. Speed up the animatin

  });
}

$(function(){
// SWIPER JS
var swiper = new Swiper(".theSwiper", {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: 3,
    spaceBetween: 50,

    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },

    // breakpoints: {
    //   // 640: {
    //   //   slidesPerView: 2,
    //   //   spaceBetween: 20,
    //   // },
    //   // 768: {
    //   //   slidesPerView: 4,
    //   //   spaceBetween: 40,
    //   // },
    //   1000: {
    //     slidesPerView: 1,
    //     spaceBetween: 80,
    //   },
    // },

  });

  // //Breakpoints
  // $(window).on('resize', function(){
  //   var width = $(window).width();
  //   if (width < 1200 && width >= 1000) {
  //     swiper.params.slidesPerView = 2;
  //     swiper.params.spaceBetween = 180;
  //   }
  //   if(width < 1000 && width >= 500) {
  //       swiper.params.slidesPerView = 1;
  //       swiper.params.spaceBetween = 50;
  //   } else if(width < 500) {
  //       swiper.params.slidesPerView = 1;
  //       swiper.params.spaceBetween = 30;
  //   } else {
  //       swiper.params.slidesPerView = 3;
  //       swiper.params.spaceBetween = 50;
  //   }
  //   swiper.update();
  // }).resize();    

});

// Wishlist Button front-end
$(function() {
    $(".heart").on("click", function() {
      $(this).toggleClass("is-active");
    });
  });


// let action2 = null;

//   $(document).ready(function() {
    
//     $(".heart").click(function() {
//         // Toggle the class "is-active"
//         $(this).toggleClass("is-active");
     
//         // Check if the clicked element has the class "is-active"
//         if ($(this).hasClass("is-active")) {
//             // If it has the class, perform some action
//             action2 = "remove";
//         } else {
//             // If it does not have the class, perform some other action
//             action2 = "add";
//         }
//     });
//     $(".heart").click();
// });

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
        const myTimeout = setTimeout(() => {location.reload()}, 700);
    })
    .catch((message) => {
        console.log(message);
    })
}






