;(function ($, w) {
	'use strict';
	if (!w.jQuery) {
		throw 'IdeaTheme: jQuery not found';
	}
	w.IdeaTheme.navigationMenu = {

		activeClass: 'active',
		bodyActiveClass: 'navigation-active',
		onNavigation: false,

		init: function () {
			this.mobile.init();
			this.createOverlay();
			this.eventListener();
		},

		mobile: {
			activeClass: 'active',
			menuRendered: false,
			mobileMenuId: 'mobile-navigation',

			init: function () {
				this.eventListener();
			},

			openSubCategories: function (element) {
				if (element.hasClass(this.activeClass)) {
					element.removeClass(this.activeClass);
				} else {
					var subCategoryHeight = element.find('> div').outerHeight();
					$('#' + this.mobileMenuId).scrollTop(0);
					$('.' + this.mobileMenuId).css('height',subCategoryHeight);
					element.addClass(this.activeClass);
				}
			},

			closeSubCategories: function (element) {
				element.parent('.has-sub-category').removeClass(this.activeClass);
				if(element.hasClass('category-level-2')) {
					$('.' + this.mobileMenuId).css('height','auto');
				}
				if(element.hasClass('category-level-3')) {
					var subCategoryHeight = element.parents('.category-level-2').outerHeight();
					$('.' + this.mobileMenuId).css('height',subCategoryHeight);
				}
			},

			toggleNavigation: function () {
				if ($('body').hasClass(IdeaTheme.navigationMenu.bodyActiveClass)) {
					$('body').removeClass(IdeaTheme.navigationMenu.bodyActiveClass);
				} else {
					$('body').addClass(IdeaTheme.navigationMenu.bodyActiveClass);
				}
			},

			eventListener: function () {
				var self = this;
				$(document).on('click', '#' + self.mobileMenuId + ' .has-sub-category a', function () {
					self.openSubCategories($(this).parent());
				});

				$(document).on('click', '.mobile-navigation-back', function () {
					self.closeSubCategories($(this).parent());
				});
			}

		},

		createOverlay: function () {
			$('body').append('<div class="navigation-menu-overlay" />');
		},
		
		overflowControl: function(element) {
			var browserWidth = $(window).width();
			var dropMenuSubCategoryLeftPosition = $(element).offset().left;
			var dropMenuSubCategoryOuterWidth = $(element).find("> div").outerWidth();
			if((browserWidth - dropMenuSubCategoryLeftPosition) < dropMenuSubCategoryOuterWidth) {
				$(element).find("> div").css({'right':'0px','left':'auto'});
			}else{
				$(element).find("> div").css({'left':'0px','right':'auto'});
			}
		},

		openDropMenu: function (element) {
			if(element.hasClass('has-sub-category')) {
				$('body').addClass(this.bodyActiveClass);
				//this.overflowControl(element);
			}
			element.addClass(this.activeClass).siblings().removeClass(this.activeClass);
		},

		closeDropMenu: function (element) {
			element.removeClass(this.activeClass);
			$('body').removeClass(this.bodyActiveClass);
		},

		eventListener: function () {
			var self = this;
			$(document).on('click', function () {
				if ($('body').hasClass(self.bodyActiveClass)) {
					$('body').removeClass(self.bodyActiveClass);
				}
			});
			
			$(document).on('mouseenter', '[data-selector="first-level-navigation"]', function() {
				var element = $(this);
				if(self.onNavigation == false) {
					window.timeout = setTimeout(function() {
						self.openDropMenu(element);
					}, 200);
				} else {
					self.openDropMenu(element);
				}
			});
			
			$(document).on('mouseleave', '[data-selector="first-level-navigation"]', function() {
				clearTimeout(window.timeout);
				self.closeDropMenu($(this));
			});

			$(document).on('mouseenter', '#navigation', function() {
				self.onNavigation = true;
			});

			$(document).on('mouseleave', '#navigation', function() {
				self.onNavigation = false;
				clearTimeout(window.timeout);
			});
		}
	}
})(jQuery, window);