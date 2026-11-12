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

/**
 * FAQ page: clicking a theme in the left menu brings that theme's questions to the top of the list
 * (the other themes stay below, in the client's order) and highlights it in the menu.
 * Also publishes one FAQPage structured-data block (all questions of the page) for search engines.
 */
add_action( 'wp_footer', function () {
	if ( ! is_page( 'faq' ) ) {
		return;
	}
	?>
	<script>
	(function () {
		var tabs = [].slice.call(document.querySelectorAll('.rcr-faq-tab'));
		var themes = [].slice.call(document.querySelectorAll('.rcr-faq-theme'));
		if (!tabs.length || !themes.length) { return; }
		var col = themes[0].parentElement;
		var bottom = col.querySelector('.rcr-faq-cta-bottom');
		if (bottom) { bottom.style.order = '99'; }
		col.style.transition = 'opacity .25s ease, transform .25s ease';
		var idOf = function (t) { return ((t.getAttribute('href') || '').split('#')[1]) || ''; };
		var mark = function (id) { tabs.forEach(function (t) { t.classList.toggle('is-active', idOf(t) === id); }); };
		var toTop = function () {
			var y = col.getBoundingClientRect().top + window.pageYOffset - 24;
			if (Math.abs(window.pageYOffset - y) > 4) { window.scrollTo({ top: y, behavior: 'smooth' }); }
		};
		var select = function (id, animate) {
			var target = document.getElementById(id);
			if (!target || themes.indexOf(target) < 0) { return; }
			mark(id);
			var apply = function () {
				themes.forEach(function (s, i) { s.style.order = (s === target) ? '-1' : String(i); });
				col.style.opacity = '1';
				col.style.transform = 'none';
				toTop();
			};
			if (animate) {
				col.style.opacity = '0';
				col.style.transform = 'translateY(10px)';
				setTimeout(apply, 200);
			} else {
				apply();
			}
		};
		mark(idOf(tabs[0]));
		document.addEventListener('click', function (e) {
			var a = e.target.closest('.rcr-faq-tab');
			if (!a) { return; }
			var id = idOf(a);
			if (!id) { return; }
			e.preventDefault();
			e.stopPropagation();
			if (history.replaceState) { history.replaceState(null, '', '#' + id); }
			select(id, true);
		}, true);
		var start = (location.hash || '').slice(1);
		if (start) { window.addEventListener('load', function () { select(start, false); }); }
	})();
	</script>
	<?php
}, 99 );

add_action( 'wp_head', function () {
	if ( ! is_page( 'faq' ) ) {
		return;
	}
	$data = json_decode( (string) get_post_meta( get_queried_object_id(), '_elementor_data', true ), true );
	if ( ! is_array( $data ) ) {
		return;
	}
	$questions = array();
	$walk      = function ( $elements ) use ( &$walk, &$questions ) {
		foreach ( $elements as $el ) {
			$type = isset( $el['widgetType'] ) ? $el['widgetType'] : '';
			$cls  = isset( $el['settings']['_css_classes'] ) ? $el['settings']['_css_classes'] : '';
			if ( 'toggle' === $type && false !== strpos( $cls, 'rcr-faqtg' ) && ! empty( $el['settings']['tabs'] ) ) {
				foreach ( $el['settings']['tabs'] as $tab ) {
					$questions[] = array(
						'@type'          => 'Question',
						'name'           => wp_strip_all_tags( $tab['tab_title'] ),
						'acceptedAnswer' => array( '@type' => 'Answer', 'text' => trim( wp_strip_all_tags( str_replace( '</p><p>', '</p> <p>', $tab['tab_content'] ) ) ) ),
					);
				}
			}
			if ( ! empty( $el['elements'] ) ) {
				$walk( $el['elements'] );
			}
		}
	};
	$walk( $data );
	if ( $questions ) {
		echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $questions ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
} );

/**
 * Home page, "Savez-vous que…": "Lire la suite" opens the full article in a pop-up instead of expanding the card.
 * The article text stays in each card's Elementor Toggle widget (edited in Elementor); the pop-up only displays it.
 */
add_action( 'wp_footer', function () {
	if ( ! is_front_page() ) {
		return;
	}
	?>
	<div class="rcr-modal" id="rcr-art-modal" hidden>
		<div class="rcr-modal-backdrop" data-close></div>
		<div class="rcr-modal-box" role="dialog" aria-modal="true" aria-labelledby="rcr-modal-title" tabindex="-1">
			<button type="button" class="rcr-modal-close" data-close aria-label="Fermer">&times;</button>
			<div class="rcr-modal-media"></div>
			<div class="rcr-modal-body">
				<div class="rcr-modal-eyebrow"></div>
				<h2 class="rcr-modal-title" id="rcr-modal-title"></h2>
				<div class="rcr-modal-intro"></div>
				<div class="rcr-modal-text"></div>
			</div>
		</div>
	</div>
	<script>
	(function () {
		var modal = document.getElementById('rcr-art-modal');
		if (!modal || !document.querySelector('.rcr-art-toggle')) { return; }
		document.body.classList.add('rcr-art-js');
		var box = modal.querySelector('.rcr-modal-box'), lastFocus = null;
		var q = function (sel) { return modal.querySelector(sel); };
		var open = function (card) {
			var img = card.querySelector('.elementor-widget-image img');
			var heads = card.querySelectorAll('.elementor-widget-heading .elementor-heading-title');
			var title = heads[heads.length - 1], eyebrow = heads.length > 1 ? heads[0] : null;
			var intro = card.querySelector('.elementor-widget-text-editor');
			var content = card.querySelector('.rcr-art-toggle .elementor-tab-content');
			q('.rcr-modal-media').innerHTML = img ? '<img src="' + (img.currentSrc || img.src) + '" alt="' + (img.alt || '').replace(/"/g, '&quot;') + '">' : '';
			q('.rcr-modal-eyebrow').textContent = eyebrow ? eyebrow.textContent : '';
			q('.rcr-modal-eyebrow').hidden = !eyebrow;
			q('.rcr-modal-title').innerHTML = title ? title.innerHTML : '';
			q('.rcr-modal-intro').innerHTML = intro ? intro.innerHTML : '';
			q('.rcr-modal-text').innerHTML = content ? content.innerHTML : '';
			lastFocus = document.activeElement;
			modal.hidden = false;
			document.documentElement.classList.add('rcr-modal-open');
			requestAnimationFrame(function () { modal.classList.add('is-open'); });
			box.scrollTop = 0;
			box.focus();
		};
		var close = function () {
			modal.classList.remove('is-open');
			document.documentElement.classList.remove('rcr-modal-open');
			setTimeout(function () { modal.hidden = true; }, 250);
			if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
		};
		var trigger = function (e) {
			var t = e.target.closest('.rcr-art-toggle .elementor-tab-title');
			if (!t) { return false; }
			e.preventDefault();
			e.stopPropagation();
			e.stopImmediatePropagation();
			open(t.closest('.rcr-art-card') || t.closest('.e-con'));
			return true;
		};
		document.addEventListener('click', trigger, true);
		document.addEventListener('keydown', function (e) {
			if (!modal.hidden && e.key === 'Escape') { close(); return; }
			if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('.rcr-art-toggle .elementor-tab-title')) { trigger(e); }
			if (!modal.hidden && e.key === 'Tab') {
				var f = [].slice.call(box.querySelectorAll('button, a[href]'));
				if (!f.length) { e.preventDefault(); return; }
				var first = f[0], last = f[f.length - 1];
				if (e.shiftKey && (document.activeElement === first || document.activeElement === box)) { e.preventDefault(); last.focus(); }
				else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
			}
		}, true);
		modal.addEventListener('click', function (e) { if (e.target.closest('[data-close]')) { close(); } });
	})();
	</script>
	<?php
}, 99 );
