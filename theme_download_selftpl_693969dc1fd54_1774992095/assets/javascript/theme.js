;(function ($, w) {
	'use strict';
	if (!w.jQuery) {
		throw 'IdeaApp: jQuery not found';
	}
	w.IdeaTheme = {

		init: function () {
			IdeaTheme.navigationMenu.init();
			IdeaTheme.cart.init();
			this.eventListener();
			this.afterInit();
		},

		afterInit: function () {
			this.cart.updateCartContainer();
			this.initLazyLoad();
			if (this[IdeaApp.helpers.getRouteGroup()] !== undefined) {
				this[IdeaApp.helpers.getRouteGroup()].init();
			}
			this.login.init();
            this.dropBox.init();
            this.bannerTitle();
            this.headerFixed();
            this.entrySlider('#entry-slider > div');
            this.categoryBannerSlider(".category-banners .row");
            this.initSecondSlider(".discounted-products .products-content");
            this.initSlider(".popular-products .products-content");
            this.listTabCarousel('.category-carousel-list-tab');
            this.initSecondSlider(".featured-products .products-content");
            this.brandsCarousel('.entry-brands-list');
            if (IdeaApp.helpers.getRouteGroup() == 'product-list' || IdeaApp.helpers.getRouteGroup() == 'combine-list') {
                this.hasFilterOption();
            }
            if (IdeaApp.helpers.getRouteName() == 'filter') {
                {% if theme.settings.display_showcase_sorting_options %}
                    this.showcaseSorting.init();
                {% endif %}
            }
		},

        hasFilterOption: function(){
            IdeaApp[IdeaApp.helpers.getRouteGroup()].filter.checkFilterMenu = function(){
                if (!IdeaApp.helpers.matchMedia('(max-width: 991px)')) {
                    $('.filter-options-title').parents('#filter-wrapper').removeClass('has-filter-option');
                    return;
                }
                if ($('.filter-menu .filter-menu-groups').length > 0 || $('.horizontal-filter-menu .filter-menu-groups').length > 0) {
                    $('.filter-options-title').parents('#filter-wrapper').addClass('has-filter-option');
                    var selectedItemCount = $('.filter-menu-selected-item').length;
                    if (selectedItemCount > 0) {
                        $('.filter-options-title span').text('(' + selectedItemCount + ')');
                    }
                }
            }
        },

        dropBox: {
            selector: '.dropbox',
            speed: 200,
            activeClass: 'active',
            targetClass: 'dropbox-content',
            closeClass: 'dropbox-close',
            activeBox: null,

            init: function () {
                this.mouseup();
                this.eventListener();
            },

            click: function (element) {
                let self = this,
                target = $('.' + element.data('target'));
                $('body').find('.dropbox-overlay').remove();
                if (element.hasClass(this.activeClass)) {
                    this.reset();
                } else {
                    switch (element.attr('data-mode')) {
                        case 'fade':
                            this.show(target);
                            break;
                        default:
                            this.slideDown(target);
                            break;
                    }
                    this.reset();
                    this.mouseup();
                    this.addClasses(element);
                    this.activeBox = element;
                    if (element.data('close')) {
                        target.append('<div class="' + self.closeClass + '" />');
                    }
                    if (element.data('overlay')) {
                        $('body').append('<div class="dropbox-overlay" />');
                        $('.dropbox-overlay').show();
                    }
                }
            },

            mouseup: function () {
                var self = this;
                $(document).bind('mouseup tap', function (e) {
                    if (!$('.' + self.targetClass).is(e.target) && $('.' + self.targetClass).has(e.target).length == 0 && !$(self.selector).is(e.target) && !$(self.selector).find('*').is(e.target)) {
                        self.reset();
                    }
                });
            },

            addClasses: function (element) {
                $(this.selector).removeClass(this.activeClass);
                $('body').addClass(element.data('target') + '-active');
                element.addClass(this.activeClass);
            },

            show: function (element) {
                element.stop(true, true).fadeIn(100);
            },

            hide: function (element) {
                element.stop(true).fadeOut(100);
            },

            slideDown: function (element) {
                element.stop(true, true).slideDown(100);
            },

            slideUp: function (element) {
                element.stop(true).slideUp(100);
            },

            reset: function () {
                if (this.activeBox) {
                    var target = this.activeBox.data('target');
                    switch (this.activeBox.data('mode')) {
                        case 'fade':
                            this.hide($('.' + target));
                            break;
                        default:
                            this.slideUp($('.' + target));
                            break;
                    }
                    $('body').removeClass(target + '-active');
                    this.activeBox = null;
                }
                $(this.selector).removeClass(this.activeClass);
                $('.dropbox-overlay').hide();
                $(document).unbind('mouseup');
            },

            eventListener: function () {
                var self = this;
                $(document).on('click tap', self.selector, function () {
                    self.click($(this));
                    if ($(this).parents('.showcase').length > 0) {
                        $(this).parents('.showcase').find('.showcase-variant-single-group-parent').parents('.showcase-variant-content').addClass('variant-loading');
                        IdeaTheme.variant.firstVariantClickControl($(this));
                    }
                });
                $(document).on('click tap', '.' + self.closeClass, function () {
                    self.reset();
                });
            }
        },

        headerFixed: function() {
            var barHeight = $('.idea-promotion-bar.bar-position-top').outerHeight() || 0;
            var headerHeight = $('#header').outerHeight();
            this.stickyOffset = barHeight + headerHeight;
            if($(window).scrollTop() > this.stickyOffset) {
                $('body').addClass('sticked');
            } else {
                $('body').removeClass('sticked');
            }
        },
        
        entrySlider: function (element) {
            if ($(element).length == 0) {
                return;
            }
            $(element).not('.slick-initialized').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                infinite: false,
                autoplay : false,
                autoplaySpeed : 6000,
                arrows : true,
                dots: true,
                swipe: true,
                speed : 300,
                fade : true,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M15 6L9 12L15 18" stroke="#747474" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 6L15 12L9 18" stroke="#747474" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            arrows: false,
                            dots: false
                        }
                    }
                ]
            });
            $(element).on('afterChange', function(event, slick, currentSlide){
                if((slick.$slides.length - slick.options.slidesToShow) <= currentSlide){
                    $(element).slick('slickPause');
                    setTimeout(function(){
                        $(element).slick('slickGoTo',0);
                        $(element).slick('slickPlay');
                    }, $(element).slick('slickGetOption', 'autoplaySpeed'));
                }
            });
        },

        categoryBannerSlider: function (element) {
            if ($(element).length == 0) {
                return;
            }
            $(element).slick({
                autoplay: true,
                autoplaySpeed: 6000,
                arrows: false,
                dots: false,
                infinite: false,
                speed: 300,
                slidesToShow: 8,
                slidesToScroll: 8,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-left" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(60.446 11.503) rotate(180)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-right" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(-54.113 0)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 6,
                            slidesToScroll: 6                                                        
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3                                                        
                        }
                    }
                ]
            });
            var dots = $(element).find('.slick-dots');
            if (dots.find('li').length <= 1) {
                dots.hide();
            }
            $(element).on('afterChange', function(event, slick, currentSlide){
                if((slick.$slides.length - slick.options.slidesToShow) <= currentSlide){
                    $(element).slick('slickPause');
                    setTimeout(function(){
                        $(element).slick('slickGoTo',0);
                        $(element).slick('slickPlay');
                    }, $(element).slick('slickGetOption', 'autoplaySpeed'));
                }
            });
        },
        
        initSlider: function (element) {
            if ($(element).length == 0) {
                return;
            }
            $(element).slick({
                autoplay: true,
                autoplaySpeed: 6000,
                arrows: false,
                dots: true,
                infinite: false,
                speed: 300,
                slidesToShow: 4,
                slidesToScroll: 4,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-left" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(60.446 11.503) rotate(180)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-right" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(-54.113 0)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3                                                        
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2                                                        
                        }
                    }
                ]
            });
            var dots = $(element).find('.slick-dots');
            if (dots.find('li').length <= 1) {
                dots.hide();
            }
            $(element).on('afterChange', function(event, slick, currentSlide){
                if((slick.$slides.length - slick.options.slidesToShow) <= currentSlide){
                    $(element).slick('slickPause');
                    setTimeout(function(){
                        $(element).slick('slickGoTo',0);
                        $(element).slick('slickPlay');
                    }, $(element).slick('slickGetOption', 'autoplaySpeed'));
                }
            });
        },

        listTabCarousel: function(element) {
            var self = this;
            var sliderOptions = {
                autoplay: false,
                arrows: false,
                dots: true,
                infinite: false,
                speed: 300,
                slidesToShow: 4,
                slidesToScroll: 4,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                            <path d="M22.2848 7L12 18L22.2848 29L24 27.1669L15.4279 18L24 8.83312L22.2848 7Z" fill="#2E3A59"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                            <path d="M13.7152 29L24 18L13.7152 7L12 8.83312L20.5721 18L12 27.1669L13.7152 29Z" fill="#2E3A59"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3                                                        
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2                                                        
                        }
                    }
                ]
            };
            var firstTab = $(element).find('[data-tab-content="1"] .products-content');
            IdeaApp.plugins.tab(element,function() {
                firstTab.slick(sliderOptions);
                firstTab.on('afterChange', function(event, slick, currentSlide) {
                    if((slick.slideCount - slick.options.slidesToShow) <= currentSlide) {
                        firstTab.slick('slickGoTo', 0);
                    }
                });
            }, function() {
                var content = $(this).attr('data-tab-index');				
                var clickedElement = $(element).find('[data-tab-content="' + content + '"] .products-content');
                if(clickedElement.hasClass('slick-initialized')) {
                    return;
                }
                clickedElement.slick(sliderOptions);
                clickedElement.on('afterChange', function(event, slick, currentSlide) {
                    if((slick.slideCount - slick.options.slidesToShow) <= currentSlide) {
                        clickedElement.slick('slickGoTo', 0);
                    }
                });
            }, function(){
                if (window.matchMedia("(max-width: 991px)").matches) {
                    $(this).parent().toggleClass('open');
                }
            });
        },

        initSecondSlider: function (element) {
            if ($(element).length == 0) {
                return;
            }
            $(element).slick({
                autoplay: true,
                autoplaySpeed: 6000,
                arrows: false,
                dots: true,
                infinite: false,
                speed: 300,
                slidesToShow: 3,
                slidesToScroll: 3,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-left" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(60.446 11.503) rotate(180)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="6.333" height="11.503" viewBox="0 0 6.333 11.503">
                            <path id="icon-arrow-right" d="M60.278,5.341,55.105.17a.581.581,0,0,0-.822.821l4.762,4.761-4.762,4.761a.581.581,0,0,0,.822.821l5.173-5.171A.586.586,0,0,0,60.278,5.341Z" transform="translate(-54.113 0)" fill="#323232"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3                                                        
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 2                                                        
                        }
                    }
                ]
            });
            var dots = $(element).find('.slick-dots');
            if (dots.find('li').length <= 1) {
                dots.hide();
            }
            $(element).on('afterChange', function(event, slick, currentSlide){
                if((slick.$slides.length - slick.options.slidesToShow) <= currentSlide){
                    $(element).slick('slickPause');
                    setTimeout(function(){
                        $(element).slick('slickGoTo',0);
                        $(element).slick('slickPlay');
                    }, $(element).slick('slickGetOption', 'autoplaySpeed'));
                }
            });
        },

        brandsCarousel: function(element) {
            var noPicImagePath = '{{ themeAsset(theme.settings.nopic_image) }}';
            brands.forEach(function(item, index) {
                var imageSrc = item.logo === null ? noPicImagePath : item.logo_path;
                var output = `
                    <div class="brands-item col-auto" data-id="${item.id}">
                        <a href="${item.link}">
                            <div><img loading="lazy" decoding="async" src="${imageSrc}"></div>
                            <span>${item.label}</span>
                        </a>
                    </div>
                `;
                $(element).append(output);
            });
            $(element).slick({
                autoplay: true,
                autoplaySpeed: 2000,
                arrows: false,
                dots: true,
                infinite: false,
                speed: 300,
                slidesToShow: 10,
                slidesToScroll: 10,
                prevArrow: `
                    <button type="button" class="slick-prev" aria-label="Previous">
                        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                            <path d="M22.2848 7L12 18L22.2848 29L24 27.1669L15.4279 18L24 8.83312L22.2848 7Z" fill="#2E3A59"/>
                        </svg>
                    </button>
                `,
                nextArrow: `
                    <button type="button" class="slick-next" aria-label="Next">
                        <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                            <path d="M13.7152 29L24 18L13.7152 7L12 8.83312L20.5721 18L12 27.1669L13.7152 29Z" fill="#2E3A59"/>
                        </svg>
                    </button>
                `,
                responsive: [
                    {
                        breakpoint: 1199,
                        settings: {
                            slidesToShow: 8,
                            slidesToScroll: 8
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 6,
                            slidesToScroll: 6
                        }
                    },
                    {
                        breakpoint: 575,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 3
                        }
                    }
                ]
            });
        },
		
		bannerTitle: function() {
			$('[data-selector="banner-title"] .banner').each(function() {
				if($(this).find('.banner-title-img').length > 0) {
					return;
				}
				var elementImg = $(this).find('img');
				elementImg.wrap('<div class="banner-title-img"></div>');
				elementImg.parent().after('<div class="banner-title-text">'+ elementImg.attr('alt') +'</div>');
			});
		},

		scrollTop: function () {
			$("html, body").animate({scrollTop: 0}, 400);
		},

		scrollToggle: function (element) {
			if (element.scrollTop() > 200) {
				$("#scroll-top").stop().fadeIn();
			} else {
				$("#scroll-top").stop().fadeOut();
			}
        },

        showcaseSorting: {
            init: function() {
                if (!document.querySelector('.showcase-container')) {
                    return;
                }
                this.mediaQueryList = window.matchMedia('(max-width: 991px)');
                this.handleMediaChange(this.mediaQueryList);
                this.mediaQueryList.addListener(this.handleMediaChange.bind(this));
                window.addEventListener('resize', this.handleResize.bind(this));
            },
        
            handleMediaChange: function(event) {
                if (event.matches) {
                    this.mobileShowcaseSorting.init();
                } else {
                    this.applyShowcaseSorting();
                }
            },
        
            handleResize: function() {
                const isMobile = this.mediaQueryList.matches;
                if (isMobile) {
                    this.mobileShowcaseSorting.init();
                } else {
                    this.applyShowcaseSorting();
                }
            },

            applyShowcaseSorting: function(){
                const self = this;
                const showcaseContainer = document.querySelector('.showcase-container');
                const sortingButtons = document.querySelectorAll('.filter-order-button span');
                self.applyLocalStorage(showcaseContainer, sortingButtons);
                sortingButtons.forEach(button => {
                    button.addEventListener("click", function() {
                        self.setActiveClass(button, sortingButtons);
                        const sortingType = button.getAttribute('data-selector');
                        showcaseContainer.className = 'showcase-container';
                        showcaseContainer.classList.add(`${sortingType}`);
                        self.setLocalStorage(sortingType);
                    });
                });
            },

            setActiveClass: function(clickedButton, sortingButtons){
                sortingButtons.forEach(button => {
                    button.classList.remove('active');
                });
                clickedButton.classList.add('active');
            },

            setLocalStorage: function(sortingType){
                localStorage.setItem('showcaseSortingType', sortingType);
            },

            applyLocalStorage: function(showcaseContainer, sortingButtons){
                const savedSortingType = localStorage.getItem('showcaseSortingType');
                if (savedSortingType) {
                    showcaseContainer.className = 'showcase-container';
                    showcaseContainer.classList.add(savedSortingType);
                    sortingButtons.forEach(button => {
                        if (button.getAttribute('data-selector') === savedSortingType) {
                            button.classList.add('active');
                        } else {
                            button.classList.remove('active');
                        }
                    });
                }
            },

            mobileShowcaseSorting: {
                init: function(){
                    this.applyShowcaseSortingOnMobile();
                },

                applyShowcaseSortingOnMobile: function(){
                    const self = this;
                    const showcaseContainer = document.querySelector('.showcase-container');
                    const sortingButtons = document.querySelectorAll('.mobile-filter-order-button span');
                    self.applyLocalStorageOnMobile(showcaseContainer, sortingButtons);
                    sortingButtons.forEach(button => {
                        button.addEventListener("click", function() {
                            self.setActiveClassOnMobile(button, sortingButtons);
                            const sortingType = button.getAttribute('data-selector');
                            showcaseContainer.className = 'showcase-container';
                            showcaseContainer.classList.add(`${sortingType}`);
                            self.setLocalStorageOnMobile(sortingType);
                        });
                    });
                },
    
                setActiveClassOnMobile: function(clickedButton, sortingButtons){
                    sortingButtons.forEach(button => {
                        button.classList.remove('active');
                    });
                    clickedButton.classList.add('active');
                },
    
                setLocalStorageOnMobile: function(sortingType){
                    localStorage.setItem('mobileShowcaseSortingType', sortingType);
                },
    
                applyLocalStorageOnMobile: function(showcaseContainer, sortingButtons){
                    const savedSortingType = localStorage.getItem('mobileShowcaseSortingType');
                    if (savedSortingType) {
                        showcaseContainer.className = 'showcase-container';
                        showcaseContainer.classList.add(savedSortingType);
                        sortingButtons.forEach(button => {
                            if (button.getAttribute('data-selector') === savedSortingType) {
                                button.classList.add('active');
                            } else {
                                button.classList.remove('active');
                            }
                        });
                    }
                }
            }
        },
		
		login: {
			init: function () {
				this.eventListener();
				this.validateLoginForm();
			},

			validateLoginForm: function () {
				var form = '[data-selector="login-panel"]';
				$(form).validate({
					errorElement: "div",
					validClass: 'validate',
					errorClass: 'validate-error',
					rules: {
						email: {
							required: true,
							email: true,
							maxlength: 255
						},
						pass: {
							required: true,
							minlength: 2,
							maxlength: 255
						},
					},
					messages: {
						email: {
							required: "{{ theme.settings.login_form_please }} " + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="email"]', 'placeholder') + " {{ theme.settings.login_form_enter }}.",
							email: "" + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="email"]', 'placeholder') + " {{ theme.settings.login_form_format }}.",
							maxlength: "" + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="email"]', 'placeholder') + " {{ theme.settings.login_form_maxlenght_255 }}."
						},
						pass: {
							required: "{{ theme.settings.login_form_please }} " + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="pass"]', 'placeholder') + " {{ theme.settings.login_form_enter }}.",
							minlength: "" + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="pass"]', 'placeholder') + " {{ theme.settings.login_form_minlenght_2 }}.",
							maxlength: "" + IdeaApp.helpers.getFormValidateMessage(form + ' input[name="pass"]', 'placeholder') + " {{ theme.settings.login_form_maxlenght_255 }}."
						}
					},
					errorPlacement: function (error, element) {
						element.parents('.user-menu-input').append(error);
					}
				});

				$.validator.addMethod('email', function (email) {
					return IdeaApp.helpers.checkEmail(email);
				});
			},

			eventListener: function () {
				$(document).on('click', '[data-selector="login-panel-button"]', function () {
					var memberLoginForm = $('[data-selector="login-panel"]');
					if (memberLoginForm.valid()) {
						$(this).addClass('btn-loading');
					}
				});
			}
		},

		cart: {
            errorLimitMessage: '{{ theme.settings.cart_limit_error_message }}',
        
            init: function () {
                this.updateCartContainer();
                this.overrideListeners();
                this.eventListener();
            },
        
            updateCartContainer: function () {
                this.cartContent();
                $('[data-selector="cart-item-count"]').html(IdeaCart.itemCount);
                $('[data-selector="cart-total-price"]').html(IdeaApp.helpers.formatMoney(IdeaCart.totalPrice) + ' ' + mainCurrency);
            },
            
            cartItemDelete: function(element) {
                IdeaCart.deleteItem(element, element.attr('data-id'));
            },
        
            cartContent: function () {
                const items = IdeaCart.items;
                const output = items.length > 0
                ? `
                    <div class="cart-content-inside">
                        <div class="cart-content-top">
                            <div class="cart-content-title">
                                <span>{{ theme.settings.cart_popup_title }}</span>
                                <div class="cart-all-delete" data-selector="cart-all-delete">{{ theme.settings.cart_popup_all_delete }}</div>
                            </div>
                            <div class="cart-content-sub-title">
                                {{ theme.settings.cart_popup_subtitle_1 }} <span>${IdeaCart.itemCount} {{ theme.settings.cart_popup_subtitle_2 }}</span> {{ theme.settings.cart_popup_subtitle_3 }}.
                            </div>
                        </div>
                        <div class="cart-content-middle">
                            <div class="cart-list">
                                ${items.map(item => {
                                    const imageUrl = item.product.imageUrl;
                                    const imageDivClass = imageUrl ? "cart-list-item-image" : "cart-list-item-image no-picture";
                                    const imageSrc = imageUrl ? imageUrl : "{{ themeAsset(theme.settings.nopic_image) }}";
                                    return `
                                        <div class="cart-list-item">
                                            <div class="${imageDivClass}">
                                                <a href="${item.product.url}">
                                                    <img src="${imageSrc}" />
                                                </a>
                                            </div>
                                            <div class="cart-list-item-content">
                                                ${item.product.brandName ? `
                                                    <div class="cart-list-item-brand">
                                                        <a href="${item.product.brandUrl}">${item.product.brandName}</a>
                                                    </div>
                                                ` : ''}
                                                <div class="cart-list-item-title">
                                                    <a href="${item.product.url}">${item.product.fullName}</a>
                                                </div>
                                                <div class="cart-list-item-price">
                                                    <span>${item.quantity}</span>
                                                    <span>${item.product.stockType}</span>
                                                    <span>-</span>
                                                    <strong>${IdeaApp.helpers.formatMoney(item.price)}</strong>
                                                    <strong>${mainCurrency}</strong>
                                                </div>
                                                <div class="cart-qty-and-delete">
                                                    <div class="cart-qty${item.product.stockAmount == 1 ? ' cart-qty-disabled' : ''}" data-selector="cart-qty-wrapper">
                                                        <a href="javascript:void(0)" class="cart-qty-minus" data-selector="cart-decrease-qty" aria-label="Decrease Quantity">
                                                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                <rect x="4.5" y="9.25" width="11" height="1.5" rx="0.75" fill="#470F00"/>
                                                            </svg>  
                                                        </a>
                                                        <input type="text" data-selector="cart-qty" data-product-id="${item.product.id}" data-id="${item.id}" data-quantity="${item.quantity}" data-stocktype="${item.product.stockType}" data-stockamount="${item.product.stockAmount}" value="${item.quantity}" aria-label="Quantity" autocomplete="off" disabled>
                                                        <a href="javascript:void(0)" class="cart-qty-plus" data-selector="cart-increase-qty" aria-label="Increase Quantity">
                                                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                <path fill-rule="evenodd" clip-rule="evenodd" d="M9.25 14.75C9.25 15.1642 9.58579 15.5 10 15.5C10.4142 15.5 10.75 15.1642 10.75 14.75V11H14.75C15.1642 11 15.5 10.6642 15.5 10.25C15.5 9.83579 15.1642 9.5 14.75 9.5H10.75V5.25C10.75 4.83579 10.4142 4.5 10 4.5C9.58579 4.5 9.25 4.83579 9.25 5.25V9.5H5.25C4.83579 9.5 4.5 9.83579 4.5 10.25C4.5 10.6642 4.83579 11 5.25 11H9.25V14.75Z" fill="#470F00"/>
                                                            </svg>
                                                        </a>
                                                    </div>
                                                    {% if theme.settings.cart_delete_check %}
                                                        <a href="javascript:void(0);" class="cart-list-item-delete" data-product-id="${item.product.id}" data-id="${item.id}" data-toggle="modal" data-target="#modal-cart-delete-${item.product.id}" data-backdrop="false">
                                                            <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.3931 8.37755C12.5068 8.26387 12.6609 8.2 12.8217 8.2H15.2341C15.3949 8.2 15.5491 8.26387 15.6628 8.37755C15.7765 8.49124 15.8403 8.64543 15.8403 8.80621V9.41241H12.2155V8.80621C12.2155 8.64543 12.2794 8.49124 12.3931 8.37755ZM11.0155 9.41241V8.80621C11.0155 8.32717 11.2058 7.86775 11.5445 7.52903C11.8833 7.1903 12.3427 7 12.8217 7H15.2341C15.7132 7 16.1726 7.1903 16.5113 7.52903C16.85 7.86775 17.0403 8.32717 17.0403 8.80621V9.41241H18.2496H19.4559C19.7872 9.41241 20.0559 9.68104 20.0559 10.0124C20.0559 10.3438 19.7872 10.6124 19.4559 10.6124H18.8496V18.4559C18.8496 18.9349 18.6594 19.3943 18.3206 19.733C17.9819 20.0718 17.5225 20.2621 17.0434 20.2621H11.0124C10.5334 20.2621 10.074 20.0718 9.73523 19.733C9.3965 19.3943 9.20621 18.9349 9.20621 18.4559V10.6124H8.6C8.26863 10.6124 8 10.3438 8 10.0124C8 9.68104 8.26863 9.41241 8.6 9.41241H9.80621H11.0155ZM10.4062 10.6124V18.4559C10.4062 18.6166 10.4701 18.7708 10.5838 18.8845C10.6974 18.9982 10.8516 19.0621 11.0124 19.0621H17.0434C17.2042 19.0621 17.3584 18.9982 17.4721 18.8845C17.5858 18.7708 17.6496 18.6166 17.6496 18.4559V10.6124H10.4062ZM12.8217 12.4279C13.1531 12.4279 13.4217 12.6966 13.4217 13.0279V16.6465C13.4217 16.9779 13.1531 17.2465 12.8217 17.2465C12.4904 17.2465 12.2217 16.9779 12.2217 16.6465V13.0279C12.2217 12.6966 12.4904 12.4279 12.8217 12.4279ZM15.8341 13.0279C15.8341 12.6966 15.5655 12.4279 15.2341 12.4279C14.9028 12.4279 14.6341 12.6966 14.6341 13.0279V16.6465C14.6341 16.9779 14.9028 17.2465 15.2341 17.2465C15.5655 17.2465 15.8341 16.9779 15.8341 16.6465V13.0279Z" fill="#110F21"/></svg>
                                                        </a>
                                                        <div class="modal-cart-delete modal fade" id="modal-cart-delete-${item.product.id}" tabindex="-1" role="dialog" aria-labelledby="modal-cart-delete-label" aria-hidden="true">
                                                            <div class="modal-dialog" role="document">
                                                                <div class="modal-content">
                                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                                                    <div class="modal-body">
                                                                        <svg width="52" height="52" viewBox="0 0 52 52" fill="none"><path d="M4.36232 41.1576C4.36394 40.578 4.51664 40.0089 4.80529 39.5065L23.1497 8.88192C23.1502 8.88113 23.1506 8.88034 23.1511 8.87956C23.4481 8.39079 23.8659 7.98666 24.3644 7.70606C24.8636 7.425 25.4268 7.27734 25.9997 7.27734C26.5726 7.27734 27.1358 7.425 27.635 7.70606C28.1334 7.98666 28.5512 8.39079 28.8483 8.87956C28.8487 8.88034 28.8492 8.88113 28.8497 8.88192L47.194 39.5064C47.4827 40.0089 47.6354 40.578 47.637 41.1576C47.6387 41.7396 47.4879 42.3119 47.1996 42.8176C46.9114 43.3232 46.4958 43.7446 45.9942 44.0398C45.494 44.3341 44.9257 44.4927 44.3455 44.5H7.65382C7.07362 44.4927 6.50533 44.3341 6.00518 44.0398C5.50355 43.7446 5.08794 43.3232 4.79971 42.8176C4.51149 42.3119 4.36069 41.7396 4.36232 41.1576Z" stroke="#F15E5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /><path d="M26 19.5V28.1667" stroke="#F15E5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /><path d="M26 36.8334H26.0217" stroke="#F15E5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /></svg>
                                                                        <span>{{ theme.settings.cart_delete_title }}</span>
                                                                    </div>
                                                                    <div class="modal-footer"><button type="button" class="btn btn-secondary btn-block" data-dismiss="modal"><span>{{ theme.settings.cart_delete_negative }}</span></button><button type="button" class="btn btn-primary" data-dismiss="modal" data-product-id="${item.product.id}" data-id="${item.id}" data-selector="cart-item-delete"><span>{{ theme.settings.cart_delete_positive }}</span></button></div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    {% else %}
                                                        <a href="javascript:void(0);" class="cart-list-item-delete" data-product-id="${item.product.id}" data-id="${item.id}" data-selector="cart-item-delete">
                                                            <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.3931 8.37755C12.5068 8.26387 12.6609 8.2 12.8217 8.2H15.2341C15.3949 8.2 15.5491 8.26387 15.6628 8.37755C15.7765 8.49124 15.8403 8.64543 15.8403 8.80621V9.41241H12.2155V8.80621C12.2155 8.64543 12.2794 8.49124 12.3931 8.37755ZM11.0155 9.41241V8.80621C11.0155 8.32717 11.2058 7.86775 11.5445 7.52903C11.8833 7.1903 12.3427 7 12.8217 7H15.2341C15.7132 7 16.1726 7.1903 16.5113 7.52903C16.85 7.86775 17.0403 8.32717 17.0403 8.80621V9.41241H18.2496H19.4559C19.7872 9.41241 20.0559 9.68104 20.0559 10.0124C20.0559 10.3438 19.7872 10.6124 19.4559 10.6124H18.8496V18.4559C18.8496 18.9349 18.6594 19.3943 18.3206 19.733C17.9819 20.0718 17.5225 20.2621 17.0434 20.2621H11.0124C10.5334 20.2621 10.074 20.0718 9.73523 19.733C9.3965 19.3943 9.20621 18.9349 9.20621 18.4559V10.6124H8.6C8.26863 10.6124 8 10.3438 8 10.0124C8 9.68104 8.26863 9.41241 8.6 9.41241H9.80621H11.0155ZM10.4062 10.6124V18.4559C10.4062 18.6166 10.4701 18.7708 10.5838 18.8845C10.6974 18.9982 10.8516 19.0621 11.0124 19.0621H17.0434C17.2042 19.0621 17.3584 18.9982 17.4721 18.8845C17.5858 18.7708 17.6496 18.6166 17.6496 18.4559V10.6124H10.4062ZM12.8217 12.4279C13.1531 12.4279 13.4217 12.6966 13.4217 13.0279V16.6465C13.4217 16.9779 13.1531 17.2465 12.8217 17.2465C12.4904 17.2465 12.2217 16.9779 12.2217 16.6465V13.0279C12.2217 12.6966 12.4904 12.4279 12.8217 12.4279ZM15.8341 13.0279C15.8341 12.6966 15.5655 12.4279 15.2341 12.4279C14.9028 12.4279 14.6341 12.6966 14.6341 13.0279V16.6465C14.6341 16.9779 14.9028 17.2465 15.2341 17.2465C15.5655 17.2465 15.8341 16.9779 15.8341 16.6465V13.0279Z" fill="#110F21"/></svg>
                                                        </a>
                                                    {% endif %}
                                                </div>
                                            </div>
                                        </div>
                                    `;
                                }).join('')}
                            </div>
                        </div>
                        <div class="cart-content-bottom">
                            <div class="cart-content-total-price">
                                <span>{{ theme.settings.cart_popup_total_title }}</span>
                                <div>${IdeaApp.helpers.formatMoney(IdeaCart.totalPrice)} ${mainCurrency}</div>
                            </div>
                            <div class="cart-content-button">
                                <a href="${IdeaApp.routing.generate('/sepet')}" class="btn btn-primary btn-block">
                                    <span>{{ theme.settings.cart_popup_buy_button }}</span>
                                </a>
                            </div>
                            <div class="cart-content-button mb-0">
                                <a href="javascript:void(0);" class="btn btn-secondary btn-block" data-selector="openbox-close">
                                    <span>{{ theme.settings.cart_popup_continue_button }}</span>
                                </a>
                            </div>
                        </div>
                    </div>
                `
                : `
                    <div class="cart-content-empty">
                        <div class="cart-content-title">{{ theme.settings.cart_popup_title }}</div>
                        <div class="cart-content-sub-title">{{ theme.settings.cart_popup_empty_title }}</div>
                        <div class="cart-content-empty-icon">
                            <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M18 4.50003C10.5442 4.50003 4.50002 10.5442 4.50002 18C4.50002 25.4559 10.5442 31.5 18 31.5C25.4559 31.5 31.5 25.4559 31.5 18C31.5 10.5442 25.4559 4.50003 18 4.50003ZM1.50002 18C1.50002 8.88734 8.88732 1.50003 18 1.50003C27.1127 1.50003 34.5 8.88734 34.5 18C34.5 27.1127 27.1127 34.5 18 34.5C8.88732 34.5 1.50002 27.1127 1.50002 18Z" fill="#2E2E2E"/>
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M34.0607 1.93934C34.6464 2.52513 34.6464 3.47487 34.0607 4.06067L4.06066 34.0607C3.47487 34.6464 2.52513 34.6464 1.93933 34.0607C1.35355 33.4749 1.35355 32.5251 1.93933 31.9394L31.9394 1.93934C32.5251 1.35355 33.4749 1.35355 34.0607 1.93934Z" fill="#2E2E2E"/>
                            </svg>
                        </div>
                        <div class="cart-content-button mb-0">
                            <a href="javascript:void(0);" class="btn btn-primary btn-block" data-selector="openbox-close"><span>{{ theme.settings.cart_popup_start_shopping_button }}</span></a>
                        </div>
                    </div>
                `;
                const cartContent = document.querySelector('[data-selector="cart-content"]');
                if (cartContent) {
                    cartContent.innerHTML = output;
                }
            },
        
            cartUpdatItem: function(element, cartItemId, quantity) {
                var self = this;
                var postUpdate = IdeaCart.listeners.postUpdate;
                IdeaCart.listeners.postUpdate = function(element, response) {
                    postUpdate(element, response);
                    IdeaCart.listeners.postUpdate = postUpdate;
                    element.parents('.cart-qty').removeClass('cart-qty-disabled');
                };
                IdeaCart.updateItem(element, cartItemId, quantity);
            },
        
            cartChangeQuantity: function(qtyElement) {
                this.cartUpdatItem(qtyElement, qtyElement.attr('data-id'), qtyElement.val());
            },
        
            cartIncrease: function(element) {
                var self = this;
                var qtyElement = element.parents('[data-selector="cart-qty-wrapper"]').find('[data-selector="cart-qty"]');
                qtyElement.parents('.cart-qty').addClass('cart-qty-disabled');
                var currentAmount = parseFloat(qtyElement.val());
                var stockAmount = parseFloat(qtyElement.attr("data-stockamount"));
                var isDecimalStockType = IdeaApp.helpers.isDecimalStockType(qtyElement.attr('data-stocktype'));
                var quantity = currentAmount;
                if (stockAmount > currentAmount) {
                    if (isDecimalStockType) {
                        quantity = currentAmount + 0.5
                    } else {
                        quantity = currentAmount + 1
                    }
                    if (isDecimalStockType) {
                        quantity = quantity.toFixed(3)
                    }
                    qtyElement.val(quantity);
                } else if (stockAmount == currentAmount) {
                    IdeaApp.plugins.notification(self.errorLimitMessage, 'warning');
                }
                self.cartChangeQuantity(qtyElement);
            },
        
            cartDecrease: function(element) {
                var self = this;
                var qtyElement = element.parents('[data-selector="cart-qty-wrapper"]').find('[data-selector="cart-qty"]');
                qtyElement.parents('.cart-qty').addClass('cart-qty-disabled');
                var currentAmount = parseFloat(qtyElement.val());
                var isDecimalStockType = IdeaApp.helpers.isDecimalStockType(qtyElement.attr('data-stocktype'));
                var decreaseAmount = isDecimalStockType ? 0.5 : 1;
                var quantity = currentAmount - decreaseAmount;
                if (quantity < decreaseAmount) {
                    quantity = decreaseAmount;
                }
                qtyElement.val(quantity.toFixed(isDecimalStockType ? 3 : 0));
                self.cartChangeQuantity(qtyElement);
            },                    
        
            showCartButtons: function (productId) {
                $('[data-selector="add-to-cart"][data-product-id="' + productId + '"]').each(function () {
                    var context = $(this).attr('data-context');
                    if (context == 'quick') {
                        $(this).attr('href', 'javascript:void(0);').removeAttr('data-disabled');
                    } else {
                        IdeaApp.helpers.enableElement($(this));
                        if (context == 'detail' || context == 'showcase') {
                            var stockContent;
                            if (context == 'detail') {
                                stockContent = `<span>{{ theme.settings.addtocart_button }}</span>`;
                                $('.quick-order-button').parent().show();
                            } else {
                                stockContent = `
                                    <span>{{ theme.settings.addtocart_button }}</span>
                                `;
                            }
                            $(this).html(stockContent).addClass('add-to-cart-button btn-primary').removeClass('no-stock-button btn-secondary');
                        }
                    }
                });
            },

            hideCartButtons: function (productId) {
                $('[data-selector="add-to-cart"][data-product-id="' + productId + '"]').each(function () {
                    var context = $(this).attr('data-context');
                    if (context == 'quick') {
                        $(this).attr('href', IdeaApp.routing.generate('/sepet')).attr('data-disabled', 'true');
                    } else {
                        IdeaApp.helpers.disableElement($(this));
                        if (context == 'detail' || context == 'showcase') { 
                            var noStockContent = context == 'showcase' ? '<span>{{ theme.settings.nostock_button }}</span>' : '<span>{{ theme.settings.nostock_button }}</span>';
                            $(this).html(noStockContent).removeClass('add-to-cart-button btn-primary').addClass('no-stock-button btn-secondary');
                            if (context == 'detail') {
                                $('.quick-order-button').parent().hide();
                            }
                        }
                    }
                });
            },
        
            showYourCartLabel: function(element, response){
                var self = this;
                const itemStockAmount = response.item.product.stockAmount;
                const itemRealAmount = itemStockAmount - response.item.quantity;
                if (itemRealAmount == 0) {
                    element.toggleClass('add-to-cart-button no-stock-button');
                }
            },
        
            overrideListeners: function () {
                var self = this;
                IdeaCart.listeners.prePersist = function (element) {
                    element.addClass('btn-loading');
                };
        
                IdeaCart.listeners.postPersist = function (element, response) {
                    element.removeClass('btn-loading');
                    if (!response.success) {
                        return;
                    }
                    self.updateCartContainer();
                    if (IdeaCart.validContextList.indexOf(element.attr('data-context')) !== -1) {
                        self.showYourCartLabel(element, response);
                        if (response.item.product.stockAmount <= IdeaCart.helpers.getItemTotalQuantity(response.item.product.id)) {
                            self.hideCartButtons(response.item.product.id);
                        }
                        {% if theme.settings.cart_fancybox %}
                            $.fancybox.open({
                                src: IdeaApp.routing.generate('/sepet-detayi'),
                                type: 'ajax'
                            });
                        {% else %}
                            $("body").append('<div class="shopping-information-cart"><div class="shopping-information-cart-inside"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle cx="26" cy="26" r="25" fill="none"/><path fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>{{ theme.settings.added_to_cart }}</div></div>');
                            setTimeout(function(){
                                $('.shopping-information-cart').fadeOut(200).remove();
                            },2000);
                        {% endif %}
                    }
                };
                IdeaCart.listeners.postUpdate = function (element, response) {
                    if (!response.success) {
                        return;
                    }
                    if (response.item.product.stockAmount <= IdeaCart.helpers.getItemTotalQuantity(response.item.product.id)) {
                        self.hideCartButtons(response.item.product.id);
                    } else {
                        self.showCartButtons(response.item.product.id);
                    }
                    self.updateCartContainer();
                };
        
                IdeaCart.listeners.preRemove = function (element) {
                    element.addClass('btn-loading');
                };
        
                IdeaCart.listeners.postRemove = function (element, response) {
                    element.removeClass('btn-loading');
                    if (!response.success) {
                        return;
                    }
                    self.showCartButtons(element.attr('data-product-id'));
                    self.updateCartContainer();
                };

                IdeaCart.listeners.postFlush = function (element, response) {
                    element.removeClass('btn-loading');
                    if (!response.success) {
                        return;
                    }
                    self.showCartButtons(element.attr('data-product-id'));
                    self.updateCartContainer();
                };
            },
        
            eventListener: function(){
                var self = this;
                $(document).on('click', '[data-selector="cart-increase-qty"]', function() {
                    self.cartIncrease($(this));
                });
                $(document).on('click', '[data-selector="cart-decrease-qty"]', function() {
                    self.cartDecrease($(this));
                });
                $(document).on('click','[data-selector="cart-all-delete"]',function() {
                    IdeaCart.flushCartItems($(this),true);
                    IdeaCart.listeners.postFlush = function () {
                        self.updateCartContainer();
                        location.reload(true);
                    };
                });
            }
        },

		initLazyLoad: function () {
			if (typeof lazyload != 'function') {
				return;
			}
			if ($('.tabbed-midblocks-container').length > 0) {
				$( document ).ajaxComplete(function( event, xhr, settings ) {
					if(settings.url == '/tabli-vitrin'){
						lazyload();
					}
				});
			} else {
				lazyload();
			}
		},
		
		footerMenu: function(element) {
			var parentElement = element.parent();
			var containerElement = element.parents('.footer-menu-container');
			if(parentElement.hasClass('active')) {
				containerElement.find('.footer-menu').removeClass('active');
				parentElement.removeClass('active');
			} else {
				containerElement.find('.footer-menu').removeClass('active');
				parentElement.addClass('active');
			}
		},

		eventListener: function () {
			var self = this;
			$(document).on('click', '#scroll-top', function () {
				self.scrollTop();
			});
			$(window).scroll(function () {
				self.scrollToggle($(this));
                self.headerFixed();
			});
			$(document).on('click tap', '[data-selector="cart-item-delete"]', function() {
				self.cart.cartItemDelete($(this))
			});
			$(document).on('click tap', '[data-selector="openbox-close"]', function() {
				openBox.reset();
			});
			$(document).on('click tap', '.search > a', function() {
				setTimeout(function(){
                    $('.search-content input').focus();
                }, 100);
			});
			$(document).on('click tap', '[data-menu-type="accordion"] .footer-menu-title', function() {
				self.footerMenu($(this));
			});
            $(document).ready(function () {
                const $marquee = $('.js-marquee');
                const content = $marquee.html();
                $marquee.append(content);
            });
		}
	}
})(jQuery, window);

$(function () {
    IdeaTheme.init();
});

document.addEventListener('DOMContentLoaded', function() {
    const btnElements = document.querySelectorAll('.btn');
    btnElements.forEach(function(element) {
        const meaningfulNodes = Array.from(element.childNodes).filter(node => {
            if (node.nodeType === 1) {
                return true;
            }
            if (node.nodeType === 3 && node.textContent.trim() !== '') {
                return true;
            }
            return false;
        });
        const isAlreadyCorrect =
            meaningfulNodes.length === 1 &&
            meaningfulNodes[0].nodeName === 'SPAN';
        if (isAlreadyCorrect) {
            return;
        }
        const wrapperSpan = document.createElement('span');
        while (element.firstChild) {
            wrapperSpan.appendChild(element.firstChild);
        }
        element.appendChild(wrapperSpan);
    });
});