import $ from 'jquery';
import 'bootstrap';

$(function () {
    // Toggle active state on contact item
    $(document).on('click', '.js-contact-list .contact-item', function () {
        $(".contact-item").removeClass("active");
        $(this).addClass("active");
    });

    // Open and close navigation
    $('.navigation-toggle').on("click", function (e) {
        e.stopPropagation();
        $('.navigation').toggleClass("navigation-visible");
    });

    $('.navigation').on("click", function (e) {
        e.stopPropagation();
    });

    $('body,html').on("click", function () {
        $('.navigation').removeClass('navigation-visible');
    });

    // Hide navigation while resize window on desktop view
    $(window).on("resize", function () {
        if ($(this).width() > 1200) {
            $('.navigation').removeClass('navigation-visible');
        }
    }).trigger('resize');

    // Hide chat
    $(".chat-hide").on("click", function () {
        $(".main").removeClass("main-visible")
    });

    // Show info panel
    $(".chat-info-toggle").on("click", function () {
        $(".chat-info").toggleClass('chat-info-visible');
    });

    // Hide info panel
    $(".chat-info-close").on("click", function () {
        $(".chat-info").removeClass("chat-info-visible");
    });

    // Scroll chat to bottom
    let scrollPos = document.querySelector('.js-scroll-to-bottom');

    if (scrollPos !== null) {
        scrollPos.scrollIntoView({
            block: 'end',
            behavior: 'instant'
        })
    };

    // Magnific popup
    $('.shared-image-list').magnificPopup({
        delegate: 'a.shared-image',
        type: 'image',
        mainClass: 'mfp-fade',
        closeOnContentClick: true,
        showCloseBtn: false,

        zoom: {
            enabled: true,
            duration: 300,
            easing: 'ease',
        },

        image: {            
            cursor: 'pointer',
        }
    });
});