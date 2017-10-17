jQuery(function ($) {

    'use strict';

    /* ---------------------------------------------- /*
     * Preloader
    /* ---------------------------------------------- */

    $(window).ready(function() {
        $('#status').fadeOut();
        $('#preloader').delay(200).fadeOut('slow');

    });


    // -------------------------------------------------------------
    // Sticky Menu
    // -------------------------------------------------------------

    (function () {
        var nav = $('.navbar');
        var scrolled = false;

        $(window).scroll(function () {

            if (110 < $(window).scrollTop() && !scrolled) {
                nav.addClass('sticky animated fadeInDown').animate({ 'margin-top': '0px' });

                scrolled = true;
            }

            if (110 > $(window).scrollTop() && scrolled) {
                nav.removeClass('sticky animated fadeInDown').css('margin-top', '0px');

                scrolled = false;
            }
        });

    }());



    // -------------------------------------------------------------
    // WOW JS
    // -------------------------------------------------------------

    (function () {
        new WOW().init();
    }());



    // -----------------------------------------------------------------
    // Smooth scrolling with sidenavbar or offcanvase using jQuery easing
    // ------------------------------------------------------------------
    $('a.appio-scroll[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');

            if (target.length) {
                $('.sidenav').removeClass('show');
                $('.sidenav-overlay').hide();
            }

        }
    });

    $('a.appio-scroll').click(function(){
        $('html, body').animate({
            scrollTop: $( $(this).attr('href') ).offset().top
        }, 1000);
        return false;
    });

    //sidenav js
    $('[data-sidenav]').sidenav();





    //-------------------------------------------------------
    // counter
    //-------------------------------------------------------

    $('.timer').each(function() {
        var $this = $(this),
            countTo = $this.attr('data-count');

        $({ countNum: $this.text()}).animate({
                countNum: countTo
            },

            {duration: 8000,
                easing:'linear',
                step: function() {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                    $this.text(this.countNum);
                }

            });

    });


    // -------------------------------------------------------------
    // Appio screenshot carousel
    // -------------------------------------------------------------
    var swiper = new Swiper('.swiper-container.appio-screen-view', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        effect: 'coverflow',
        loop: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        autoplay: 2000,
        autoplayDisableOnInteraction: true,
        coverflow: {
            rotate: 0,
            stretch: 150,
            modifier: 1.5,
            slideShadows : false
        }
    });



    // -------------------------------------------------------------
    // Detect IE version
    // -------------------------------------------------------------
    (function () {
        function getIEVersion() {
            var match = navigator.userAgent.match(/(?:MSIE |Trident\/.*; rv:)(\d+)/);
            return match ? parseInt(match[1]) : false;
        }


        if( getIEVersion() ){
            $('html').addClass('ie'+getIEVersion());
        }


        if( $('html').hasClass('ie9') || $('html').hasClass('ie10')  ){

            $('.submenu-wrapper').each(function(){

               $(this).addClass('no-pointer-events');

            });

        }

    }());




    // ------------------------------------------------------------------
    // jQuery for back to Top
    // ------------------------------------------------------------------

    (function(){

        $('body').append('<div id="toTop"><span>Up</span></div>');

        $(window).scroll(function () {
            if ($(this).scrollTop() != 0) {
                $('#toTop').fadeIn();
            } else {
                $('#toTop').fadeOut();
            }
        });

        $('#toTop').on('click',function(){
            $("html, body").animate({ scrollTop: 0 }, 600);
            return false;
        });

    }());



	// -----------------------------------------------------------------
	//CONTACT FORM & SUBSCRIPTION FORM VALIDATOR
	// -----------------------------------------------------------------

    $('#contact-form').validator();


    /*----- Subscription Form ----- */
    $('#contact-form').validator();



    /// -----------------------------------------------------------------
    // TESTIMONIAL CAROUSEL
    // -----------------------------------------------------------------
    $('.appio-owl-testimonial').owlCarousel({
        center: true,
        items: 2,
        autoplay: true,
        dots: true,
        loop: true,
        autoplayTimeout:9000,
        autoplaySpeed : 5000,
        responsive:{
            0:{
                items:1,
                nav:false
            }
        }
    });


    // -----------------------------------------------------------------
    //Magnific VIDEO Popup
    // -----------------------------------------------------------------

    $('.video').magnificPopup({
        type: 'iframe'
    });




}); // JQuery end