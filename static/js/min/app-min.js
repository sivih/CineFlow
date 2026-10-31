(function($, document, window) {
  $(document).ready(function() {
    // 1. Clone the main navigation menu into mobile navigation
    $(".mobile-navigation").append($(".main-navigation .menu").clone());

    // 2. Toggle mobile navigation menu when menu button is clicked
    $(".menu-toggle").click(function() {
      $(".mobile-navigation").slideToggle();
    });

    // 3. Search form interaction - show/hide input on button click
    $(".search-form button").click(function() {
      $(this).toggleClass("active");
      var form = $(this).parent(".search-form");
      form.find("input").toggleClass("active").focus();
    });

    // 4. Initialize FlexSlider for any .slider elements
    $(".slider").flexslider({
      controlNav: false,
      prevText: '<i class="fa fa-chevron-left"></i>',
      nextText: '<i class="fa fa-chevron-right"></i>'
    });

    // 5. Initialize Google Maps if a .map element exists
    if ($(".map").length) {
      $(".map").gmap3({
        map: {
          options: {
            maxZoom: 14
          }
        },
        marker: {
          address: "40 Sibley St, Detroit"
        }
      }, "autofit");
    }
  });

  // 6. Placeholder for code that runs on full page load (currently empty)
  $(window).on("load", function() {
    // Nothing here yet
  });

})(jQuery, document, window);
