// JavaScript Document

(function($) {
    "use strict";
	
	
	//calling Brand Crousel
	$(".main-banner").owlCarousel({
		loop:true,
		margin:5,
		responsiveClass:true,
		slideSpeed : 2000,
		smartSpeed:2500,
		nav: true,
		autoplay: true,
		autoplayTimeout:5000,
		responsiveRefreshRate : 200,
		rewind:true,
		responsive:{
			0:{
				items:1,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
			},
			600:{
				items:1,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
			},
			1000:{
				items:1,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
				loop:true
			}
		}
	});
	
	
	//testimonials Crousel
	var owl = $('.testimonials');
		owl.owlCarousel({
		items:1,
		loop:true,
		margin:5,
		autoplay: true,
		smartSpeed:4000,
		autoplayTimeout:5000,
		autoplayHoverPause:true
	});


	//Our Staff Page Crousel
	$(".our-staff-page").owlCarousel({
		loop:true,
		margin:15,
		responsiveClass:true,
		autoplay: true,
		smartSpeed:4000,
		slideSpeed : 2000,
		smartSpeed:2500,
		nav: true,
		responsiveRefreshRate : 200,
		rewind:true,
		responsive:{
			0:{
				items:1,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
			},
			600:{
				items:2,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
			},
			1000:{
				items:4,
				nav:false,
				navText:["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
				loop:true
			}
		}
	});
	
	
	//OnScroll Animation Appear
	$('.animated').appear(function() {

		var elem = $(this);
		var animation = elem.data('animation');

		if ( !elem.hasClass('visible') ) {
			var animationDelay = elem.data('animation-delay');
			if ( animationDelay ) {
				setTimeout(function(){
					elem.addClass( animation + " visible" );
				}, animationDelay);

			} else {
				elem.addClass( animation + " visible" );
			}
		}

	});


	//Saying page loaded
	$(window).on("load",function(){
		$("body").addClass("loaded");
		$(".preloader").html("");
		$(".preloader").css("display", "none");
	 });

	
	//Display Scroll Btn on 1000px
	$(window).on("scroll",function() { 
		if($(this).scrollTop() > 1000) { 
			$("#top").fadeIn();
		} else { 
			$("#top").fadeOut();
		}
	});

	
	//scroll effect
	$("#top").on("click",function () {
		$("html, body").animate({ scrollTop: 0 }, "slow");
		return false;
	});        

	
	//Moving Top 
	$("#top").on("click",function (event) {
		event.stopPropagation();                
		var idTo = $(this).attr("data-atr");                
		var Position = $("[id='" + idTo + "']").offset();
		$("html, body").animate({ scrollTop: Position }, "slow");
		return false;
	});

	
	// video-preview-one
	$(document).ready(function() {
		$('.video-preview').magnificPopup({
			disableOn: 700,
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false
		});
	});

	
	//navigation Scroll 300px
	$(window).on('scroll', function() {

		var b = $(window).scrollTop();

		if( b > 350 ){		
			$(".sticky-navigation").addClass("fixed-top");
		} else {
			$(".sticky-navigation").removeClass("fixed-top");
		}				

	});
	

	// Lightbox Gallery
	$(document).ready(function() {
		$('.portfolio-gallery').magnificPopup({
			delegate: 'a',
			type: 'image',
			tLoading: 'Loading image #%curr%...',
			mainClass: 'mfp-img-mobile',
			gallery: {
				enabled: true,
				navigateByImgClick: true,
				preload: [0,1] // Will preload 0 - before current, and 1 after the current image
			},
			image: {
				tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
				titleSrc: function(item) {
					return item.el.attr('title') + '<small>Education Buddy</small>';
				}
			}
		});
	});

	
	// JavaScript for disabling form submissions if there are invalid fields
	(function() {
	  'use strict';
	  window.addEventListener('load', function() {
		// Fetch all the forms we want to apply custom Bootstrap validation styles to
		var forms = document.getElementsByClassName('needs-validation');
		// Loop over them and prevent submission
		var validation = Array.prototype.filter.call(forms, function(form) {
		  form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
			  event.preventDefault();
			  event.stopPropagation();
			}
			form.classList.add('was-validated');
		  }, false);
		});
	  }, false);
	})();
	
})(jQuery); //jQuery main function ends strict Mode on