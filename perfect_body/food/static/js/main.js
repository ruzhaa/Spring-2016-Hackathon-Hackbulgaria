(function() {
		$('dd').filter(':nth-child(n+2)').addClass('hide');
		$('dl').on('mouseenter', 'dt', function() {
			$(this)
				.next()
					.slideDown(300)
					.siblings('dd')
						.slideUp(300);

		})

	})();