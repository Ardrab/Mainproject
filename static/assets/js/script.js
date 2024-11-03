$( document ).ready(function() {
    var w = window.innerWidth;
   
    if(w > 767){
        $('#nav-head').scrollToFixed();
    }else{
        $('#nav-head').scrollToFixed();
    }
    
})


$( document ).ready(function() {

     $('.owl-carousel').owlCarousel({
        loop:true,
        margin:0,
        nav:true,
        autoplay: true,
        dots: true,
        autoplayTimeout: 5000,
        navText:['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        responsive:{
            0:{
                items:1
            },
            600:{
                items:1
            },
            1000:{
                items:1
            }
        }
    })


});

$(document).ready(function(){

    $(".filter-button").click(function(){
        var value = $(this).attr('data-filter');
        
        if(value == "all")
        {
            //$('.filter').removeClass('hidden');
            $('.filter').show('1000');
        }
        else
        {
//            $('.filter[filter-item="'+value+'"]').removeClass('hidden');
//            $(".filter").not('.filter[filter-item="'+value+'"]').addClass('hidden');
            $(".filter").not('.'+value).hide('3000');
            $('.filter').filter('.'+value).show('3000');
            
        }
    });
    
    if ($(".filter-button").removeClass("active")) {
$(this).removeClass("active");
}
$(this).addClass("active");

});

// script.js

// Function to prevent users from going back to userindex.html after logout
(function () {
    // Check if the current page is userindex.html
    if (window.location.pathname.includes('/user/userindex/')) {
        // Listen for the page to be loaded
        window.addEventListener('load', function () {
            // Get the session storage item indicating logout
            var logout = sessionStorage.getItem('logout');

            // If logout is true, redirect to index.html
            if (logout === 'true') {
                sessionStorage.removeItem('logout'); // Clear logout flag
                window.location.href = '/';  // Redirect to the homepage
            }
        });
    }

    // Disable back button after logout
    window.addEventListener('load', function () {
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }
    });

    // Intercept back/forward button functionality after logout
    window.addEventListener('popstate', function () {
        window.history.pushState(null, null, window.location.href);
    });
})();
