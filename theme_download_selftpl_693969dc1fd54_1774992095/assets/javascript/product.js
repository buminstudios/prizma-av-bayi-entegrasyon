;(function ($, w) {
	'use strict';
	if (!w.jQuery) {
		throw 'IdeaApp: jQuery not found';
	}
	w.IdeaTheme.product = {

		init: function () {
			this.eventListener();
			this.thumbImagesCarousel();
			this.zoom.init();
			this.afterInit();
		},

		afterInit: function () {
			IdeaTheme.initSlider('.similar-products .products-content');
			IdeaTheme.initSlider('.offered-products .products-content');
			IdeaTheme.initSlider('.combined-products .products-content');
			IdeaTheme.initLazyLoad();
            this.responsiveTabs();
            this.allButtonAddSpan();
            this.commentRate();
        },

        allButtonAddSpan: function() {
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
        },

        responsiveTabs: function(){
            IdeaApp.product.productTab('.product-detail-tab', function () {}, function () {});
            $('.product-detail-tab-row [data-tab-index]').on('click', function(event) {
                if($(this).parent().attr('class').indexOf('active') > -1) {
                    $(this).next().slideUp();
                    $(this).parent().removeClass('active');
                } else {
                    $(this).next().slideDown().parent().siblings().find('[data-tab-content]').slideUp();
                    $('.product-detail-tab-row').removeClass('active');
                    $(this).parent().addClass('active');
                }
                $('html, body').animate({
                    scrollTop: $(this).parent().parent().offset().top - 15
                }, 500);
            });
            {% if theme.settings.product_detail_mobile_first_tab %}
                $('.product-detail-tab-content .product-detail-tab-row.active .active[data-tab-content]').show();
            {% endif %}
            var productId = $('.product-detail-tab').attr('data-product-id');
            $.ajax({
                url: '/taksit-secenekleri',
                data: "productId=" + productId,
                success: function (response) {
                    $('[data-selector="product-payment-options"]').html(response);
                }
            });
        },

		thumbImagesCarousel: function () {
			$('#product-thumb-image').slick({
				vertical: false,
				verticalSwiping: false,
				autoplay: false,
				arrows: false,
				infinite: false,
				speed: 300,
				slidesToShow: 6,
				slidesToScroll: 6,
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
                            slidesToShow: 5,
                            slidesToScroll: 5
                        }
                    }
                ]
			});
		},

        commentRate: function() {
            $('.product-comment-rating').rateYo({
                rating: $('.product-comment-rating').attr('data-rank'),
                starWidth : "16px",
                normalFill: "#EDEDED",
                ratedFill : "#FFC107"
            });
        },

		zoom: {
			config: {
				gallery: 'product-thumb-image',
				responsive: true,
				zoomType: "inner",
				borderSize: 0,
				cursor: 'crosshair',
				onZoomedImageLoaded: function () {
					$('#primary-image').unbind('touchmove mousewheel');
					if($('#product-thumb-image .thumb-item a.zoomGalleryActive').length < 1) {
						$('#product-thumb-image .thumb-item:first-child a').addClass('zoomGalleryActive');
					}
				}
			},
			init: function() {
				$('.zoomContainer').remove();
				$('#primary-image').elevateZoom(this.config);
				this.eventListener();
			},
			eventListener: function() {
				var self = this;
				$('#primary-image, .product-image-item a').on('click', function (e) {
                    e.preventDefault();
                    var ez = $(this).data('elevateZoom');
                    if (ez) {
                        $.fancybox.open(ez.getGalleryList(), {
                            i18n: {
                                en: {
                                    SHARE: "{{ theme.settings.fancybox_share }}"
                                }
                            }
                        });
                    } else {
                        $.fancybox.open(
                            $('[data-fancybox="gallery"]').map(function () {
                                return {
                                    src: $(this).attr('href'),
                                    type: 'image'
                                };
                            }).get(),
                            {
                                i18n: {
                                    en: {
                                        SHARE: "{{ theme.settings.fancybox_share }}"
                                    }
                                }
                            },
                            $('[data-fancybox="gallery"]').index(this)
                        );
                    }
                });
				$('#product-thumb-image .thumb-item a').on('click tap', function() {
					var image = $('#primary-image');
					$('.zoomContainer').remove();
					image.removeData('elevateZoom').attr('src', $(this).data('image')).data('zoom-image', $(this).data('zoom-image')).elevateZoom(IdeaTheme.product.zoom.config);
				});
			}
		},

		eventListener: function () {
			var self = this;
		}
	}
})(jQuery, window);