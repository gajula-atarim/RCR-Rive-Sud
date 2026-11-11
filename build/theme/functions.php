<?php
/**
 * Hello Elementor Child functions.
 */

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );
	wp_enqueue_style(
		'rcr-fonts',
		'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Source+Sans+3:wght@400;500;600;700&display=swap',
		array(),
		null
	);
	wp_enqueue_style(
		'rcr-child',
		get_stylesheet_uri(),
		array( 'parent-style' ),
		filemtime( get_stylesheet_directory() . '/style.css' )
	);
}, 20 );

/**
 * Allow SVG uploads on every upload route (including the REST/MCP route Atarim uses) for the
 * roles enabled in Safe SVG (Settings > Media > Safe SVG > User Roles). Safe SVG still
 * sanitizes each SVG on upload; without Safe SVG active this filter does nothing.
 */
add_filter( 'upload_mimes', function ( $mimes ) {
	if ( class_exists( '\SafeSvg\Svg_Sanitizer' ) && \SafeSvg\Svg_Sanitizer::current_user_can_upload() ) {
		$mimes['svg'] = 'image/svg+xml';
	}
	return $mimes;
} );

/**
 * The site is French only: declare the page language as French (fr-CA) on every front-end page so
 * browsers, screen readers and search engines read it correctly, and add an "rcr-lang-fr" body class
 * used by style.css for French typography rules.
 */
function rcr_is_french_page() {
	return ! is_admin();
}
add_filter( 'language_attributes', function ( $output ) {
	if ( rcr_is_french_page() ) {
		$output = preg_replace( '/lang="[^"]*"/', 'lang="fr-CA"', $output );
	}
	return $output;
} );
add_filter( 'body_class', function ( $classes ) {
	if ( rcr_is_french_page() ) {
		$classes[] = 'rcr-lang-fr';
	}
	return $classes;
} );

/**
 * "Ce que vous apprendrez" (home page): clicking or pressing Enter on a round image opens the
 * "En savoir plus" toggle of the same column. The toggles themselves are Elementor Toggle widgets.
 */
add_action( 'wp_footer', function () {
	if ( ! is_front_page() ) {
		return;
	}
	?>
	<script>
	(function () {
		document.querySelectorAll('.rcr-step-trigger').forEach(function (el) {
			var col = el.closest('.rcr-step');
			var title = col && col.querySelector('.elementor-tab-title');
			if (!title) { return; }
			var label = (col.querySelector('h3') || {}).textContent || '';
			el.setAttribute('role', 'button');
			el.setAttribute('tabindex', '0');
			el.setAttribute('aria-label', 'En savoir plus : ' + label.trim());
			var open = function () { title.click(); };
			el.addEventListener('click', open);
			el.addEventListener('keydown', function (e) {
				if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
			});
		});
	})();
	</script>
	<?php
}, 99 );

/**
 * Services page: show one service at a time, like the design (pills, sidebar list and
 * previous/next buttons). Every service is a normal Elementor container with its own anchor
 * (#cardio-secours, #sir, #anaphylaxie, #sur-place, #tarifs); without this script they are all shown.
 */
add_action( 'wp_footer', function () {
	if ( ! is_page( 'services' ) ) {
		return;
	}
	?>
	<script>
	(function () {
		var root = document.querySelector('.rcr-svc');
		if (!root) { return; }
		var panels = [].slice.call(root.querySelectorAll('.rcr-svc-panel'));
		if (!panels.length) { return; }
		var ids = panels.map(function (p) { return p.id; });
		var wrap = root.querySelector('.rcr-svc-panels');
		var pills = [].slice.call(root.querySelectorAll('.rcr-svc-pill'));
		var tabs = [].slice.call(root.querySelectorAll('.rcr-svc-tab'));
		var prev = root.querySelector('.rcr-svc-prev'), next = root.querySelector('.rcr-svc-next');
		var pos = root.querySelector('.rcr-svc-pos'), crumb = document.querySelector('.rcr-banner .rcr-cur');
		var main = root.querySelector('.rcr-svc-main');
		var labels = {}, cur = null;
		var linkId = function (el) {
			var a = el.matches('a') ? el : el.querySelector('a');
			return a ? ((a.getAttribute('href') || '').split('#')[1] || '') : '';
		};
		tabs.forEach(function (t) {
			var l = t.querySelector('.rcr-svc-tab-label .elementor-heading-title');
			if (l) { labels[linkId(t)] = l.textContent.trim(); }
		});
		var setNav = function (box, id) {
			if (!box) { return; }
			if (!id) { box.classList.add('is-hidden'); box.setAttribute('href', '#'); box.setAttribute('tabindex', '-1'); return; }
			box.classList.remove('is-hidden'); box.removeAttribute('tabindex'); box.setAttribute('href', '#' + id);
			var l = box.querySelector('.rcr-svc-label .elementor-heading-title');
			if (l) { l.textContent = labels[id] || ''; }
		};
		var scrollUp = function () {
			if (!main) { return; }
			var y = main.getBoundingClientRect().top + window.pageYOffset - 20;
			if (window.pageYOffset > y) { window.scrollTo({ top: y, behavior: 'smooth' }); }
		};
		var show = function (id, scroll) {
			if (ids.indexOf(id) < 0) { id = ids[0]; }
			var i = ids.indexOf(id);
			var apply = function () {
				panels.forEach(function (p) { p.classList.toggle('is-active', p.id === id); });
				pills.forEach(function (p) { p.classList.toggle('is-active', linkId(p) === id); });
				tabs.forEach(function (t) {
					var on = linkId(t) === id;
					t.classList.toggle('is-active', on);
					if (on) { t.setAttribute('aria-current', 'true'); } else { t.removeAttribute('aria-current'); }
				});
				if (pos) { pos.textContent = i + 1; }
				if (crumb) { crumb.textContent = labels[id] || ''; }
				setNav(prev, ids[i - 1]);
				setNav(next, ids[i + 1]);
				cur = id;
			};
			if (cur && cur !== id && wrap) {
				wrap.classList.add('is-fading');
				setTimeout(function () { apply(); wrap.classList.remove('is-fading'); if (scroll) { scrollUp(); } }, 180);
			} else {
				apply();
				if (scroll) { scrollUp(); }
			}
		};
		document.body.classList.add('rcr-svc-js');
		root.addEventListener('click', function (e) {
			var a = e.target.closest('a');
			if (!a || !root.contains(a)) { return; }
			var href = a.getAttribute('href') || '';
			if (href.charAt(0) !== '#') { return; }
			var id = href.slice(1);
			if (ids.indexOf(id) < 0) { if (!id) { e.preventDefault(); } return; }
			e.preventDefault();
			e.stopPropagation();
			if (history.replaceState) { history.replaceState(null, '', '#' + id); }
			show(id, true);
		}, true);
		show((location.hash || '').slice(1), false);
		window.addEventListener('hashchange', function () { show(location.hash.slice(1), true); });
	})();
	</script>
	<?php
}, 99 );
