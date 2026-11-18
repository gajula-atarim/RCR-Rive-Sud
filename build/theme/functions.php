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
 * Languages (Polylang): French is the main language (/), English lives under /en/.
 * rcr_lang() returns "fr" or "en" for the page being shown; the <html lang> attribute and an
 * "rcr-lang-fr" / "rcr-lang-en" body class follow it (style.css uses the class for typography rules).
 */
function rcr_lang() {
	if ( function_exists( 'pll_current_language' ) ) {
		$l = pll_current_language( 'slug' );
		if ( $l ) {
			return $l;
		}
	}
	return 'fr';
}
function rcr_is_french_page() {
	return ! is_admin() && 'en' !== rcr_lang();
}
/** True on the page with this (French) ID or on its English translation. */
function rcr_is_page_tr( $fr_id ) {
	if ( ! is_page() ) {
		return false;
	}
	$id = get_queried_object_id();
	if ( (int) $id === (int) $fr_id ) {
		return true;
	}
	return function_exists( 'pll_get_post' ) && (int) pll_get_post( $fr_id, 'en' ) === (int) $id;
}
add_filter( 'language_attributes', function ( $output ) {
	if ( is_admin() ) {
		return $output;
	}
	$lang = 'en' === rcr_lang() ? 'en-CA' : 'fr-CA';
	return preg_match( '/lang="[^"]*"/', $output ) ? preg_replace( '/lang="[^"]*"/', 'lang="' . $lang . '"', $output ) : $output . ' lang="' . $lang . '"';
} );
add_filter( 'body_class', function ( $classes ) {
	if ( ! is_admin() ) {
		$classes[] = 'en' === rcr_lang() ? 'rcr-lang-en' : 'rcr-lang-fr';
	}
	return $classes;
} );

/** English tagline (the site title "RCR Rive-Sud" is the same in both languages). */
add_filter( 'option_blogdescription', function ( $value ) {
	return ( ! is_admin() && 'en' === rcr_lang() ) ? 'CPR training on Montreal’s South Shore' : $value;
} );

/**
 * Image alt texts: media items are shared by both languages and hold the French alt text; on English
 * pages the English alt text saved in the "rcr_en_alts" option (media ID => text) is used instead.
 */
add_filter( 'get_post_metadata', function ( $value, $object_id, $meta_key ) {
	if ( '_wp_attachment_image_alt' !== $meta_key || is_admin() || 'en' !== rcr_lang() ) {
		return $value;
	}
	$alts = get_option( 'rcr_en_alts' );
	return ( is_array( $alts ) && ! empty( $alts[ $object_id ] ) ) ? array( $alts[ $object_id ] ) : $value;
}, 10, 3 );

/**
 * Header FR / EN buttons: point each one to the same page in that language (Polylang prints the
 * addresses as <link rel="alternate" hreflang> tags); without a translation they go to that language's home.
 */
add_action( 'wp_footer', function () {
	?>
	<script>
	(function () {
		var homes = { fr: '<?php echo esc_js( home_url( '/' ) ); ?>', en: '<?php echo esc_js( home_url( '/en/' ) ); ?>' };
		var alt = {};
		document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function (l) {
			var h = (l.getAttribute('hreflang') || '').slice(0, 2).toLowerCase();
			if (homes[h]) { alt[h] = l.href; }
		});
		document.querySelectorAll('.elementor-location-header a, header a, .ehf-header a').forEach(function (a) {
			var t = (a.textContent || '').trim().toLowerCase();
			if (t === 'fr' || t === 'en') {
				a.setAttribute('href', alt[t] || homes[t]);
				a.setAttribute('hreflang', t);
				a.setAttribute('lang', t);
			}
		});
	})();
	</script>
	<?php
}, 99 );

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
			el.setAttribute('aria-label', <?php echo wp_json_encode( 'en' === rcr_lang() ? 'Learn more: ' : 'En savoir plus : ' ); ?> + label.trim());
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
	if ( ! rcr_is_page_tr( 507 ) ) {
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
	if ( ! rcr_is_page_tr( 509 ) ) {
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
	if ( ! rcr_is_page_tr( 509 ) ) {
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
 * Home page, "Savez-vous que…" / "Did you know…": "Lire la suite" / "Read more" opens the full article in a pop-up instead of expanding the card.
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
			<button type="button" class="rcr-modal-close" data-close aria-label="<?php echo esc_attr( 'en' === rcr_lang() ? 'Close' : 'Fermer' ); ?>">&times;</button>
			<div class="rcr-modal-side">
				<div class="rcr-modal-media"></div>
				<div class="rcr-modal-eyebrow"></div>
				<h2 class="rcr-modal-title" id="rcr-modal-title"></h2>
			</div>
			<div class="rcr-modal-body">
				<div class="rcr-modal-intro"></div>
				<div class="rcr-modal-rule"></div>
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
			var b = q('.rcr-modal-body'); if (b) { b.scrollTop = 0; }
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

/**
 * TEMPORARY one-shot English builder (removed right after it runs).
 * ?rcr_i18n=lang   creates the Polylang languages (French default at /, English at /en/)
 * ?rcr_i18n=assign marks every existing post, page and term as French
 * ?rcr_i18n=build  creates the English pages, header, footer, menu and contact form from the French ones
 * Each step writes a short report to wp-content/uploads/rcr-i18n/log.txt.
 */
add_action( 'wp_loaded', function () {
	$step = isset( $_GET['rcr_i18n'] ) ? sanitize_key( $_GET['rcr_i18n'] ) : '';
	if ( 'rebuild' === $step && get_option( 'rcr_i18n_done_rebuild2' ) ) {
		return;
	}
	if ( 'rebuild' === $step ) {
		delete_option( 'rcr_i18n_done_build' );
		$step = 'build';
	}
	if ( ! in_array( $step, array( 'lang', 'assign', 'build', 'hf1', 'hf2', 'front3', 'front4' ), true ) || get_option( 'rcr_i18n_done_' . $step ) ) {
		return;
	}
	$dir = wp_upload_dir()['basedir'] . '/rcr-i18n';
	wp_mkdir_p( $dir );
	$log = array();
	$say = function ( $m ) use ( &$log ) {
		$log[] = is_string( $m ) ? $m : wp_json_encode( $m, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	};
	try {
		if ( 'lang' === $step ) {
			$langs = array(
				array( 'name' => 'Français', 'slug' => 'fr', 'locale' => 'fr_CA', 'rtl' => false, 'term_group' => 0, 'flag' => 'ca' ),
				array( 'name' => 'English', 'slug' => 'en', 'locale' => 'en_CA', 'rtl' => false, 'term_group' => 1, 'flag' => 'ca' ),
			);
			$model = null;
			if ( isset( $GLOBALS['polylang'] ) && isset( $GLOBALS['polylang']->model ) ) {
				$model = $GLOBALS['polylang']->model;
				$say( 'model from PLL(): ' . get_class( $model ) );
			}
			if ( ! $model && class_exists( 'PLL_Admin_Model' ) ) {
				$opt   = class_exists( '\WP_Syntex\Polylang\Options\Options' ) ? new \WP_Syntex\Polylang\Options\Options() : get_option( 'polylang' );
				$model = new PLL_Admin_Model( $opt );
				$say( 'model built: PLL_Admin_Model' );
			}
			foreach ( $langs as $l ) {
				$exists = $model && method_exists( $model, 'get_language' ) ? $model->get_language( $l['slug'] ) : false;
				if ( $exists ) {
					$say( 'exists ' . $l['slug'] );
					continue;
				}
				if ( isset( $model->languages ) && is_object( $model->languages ) && method_exists( $model->languages, 'add' ) ) {
					$r = $model->languages->add( $l );
					$say( 'languages->add ' . $l['slug'] . ': ' . ( is_wp_error( $r ) ? $r->get_error_message() : wp_json_encode( $r ) ) );
				} elseif ( method_exists( $model, 'add_language' ) ) {
					$r = $model->add_language( $l );
					$say( 'add_language ' . $l['slug'] . ': ' . ( is_wp_error( $r ) ? $r->get_error_message() : wp_json_encode( $r ) ) );
				} else {
					$say( 'no API to add a language' );
				}
			}
			$o = get_option( 'polylang' );
			if ( is_array( $o ) ) {
				$o['default_lang']  = 'fr';
				$o['force_lang']    = 1;
				$o['hide_default']  = true;
				$o['rewrite']       = true;
				$o['redirect_lang'] = true;
				$o['browser']       = false;
				update_option( 'polylang', $o );
			}
			delete_transient( 'pll_languages_list' );
			flush_rewrite_rules( false );
			$say( array( 'options' => get_option( 'polylang' ) ) );
			$say( array( 'terms' => wp_list_pluck( get_terms( array( 'taxonomy' => 'language', 'hide_empty' => false ) ), 'slug' ) ) );
		}

		if ( 'assign' === $step ) {
			if ( ! function_exists( 'pll_set_post_language' ) ) {
				throw new Exception( 'Polylang functions not loaded (no languages yet?)' );
			}
			$n = 0;
			foreach ( get_posts( array( 'post_type' => array( 'page', 'post' ), 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids', 'lang' => '', 'suppress_filters' => false ) ) as $id ) {
				if ( ! pll_get_post_language( $id ) ) {
					pll_set_post_language( $id, 'fr' );
					$n++;
				}
			}
			$t = 0;
			foreach ( get_terms( array( 'taxonomy' => array( 'category', 'post_tag' ), 'hide_empty' => false, 'fields' => 'ids', 'lang' => '' ) ) as $tid ) {
				if ( ! pll_get_term_language( $tid ) ) {
					pll_set_term_language( $tid, 'fr' );
					$t++;
				}
			}
			$say( "posts set to fr: $n, terms: $t" );
			$say( array( 'front' => get_option( 'page_on_front' ), 'front_lang' => pll_get_post_language( (int) get_option( 'page_on_front' ) ) ) );
		}

		if ( 'build' === $step ) {
			if ( ! function_exists( 'pll_save_post_translations' ) ) {
				throw new Exception( 'Polylang functions not loaded' );
			}
			$res = wp_remote_get( 'https://raw.githubusercontent.com/gajula-atarim/RCR-Rive-Sud/01cc07a8dc9d16e5042738c500f315916bbebab5/build/i18n/out/en_map.json', array( 'timeout' => 30 ) );
			$map = json_decode( is_wp_error( $res ) ? '' : wp_remote_retrieve_body( $res ), true );
			if ( ! is_array( $map ) || empty( $map['strings'] ) ) {
				throw new Exception( 'map not loaded' );
			}
			$ids  = (array) get_option( 'rcr_en_ids', array() );
			$home = untrailingslashit( home_url() );
			$url  = function ( $u ) use ( $map, $home ) {
				if ( ! is_string( $u ) || '' === $u ) {
					return $u;
				}
				$rel = 0 === strpos( $u, $home ) ? substr( $u, strlen( $home ) ) : $u;
				if ( '' === $rel ) {
					$rel = '/';
				}
				$hash = '';
				if ( false !== ( $p = strpos( $rel, '#' ) ) ) {
					$hash = substr( $rel, $p + 1 );
					$rel  = substr( $rel, 0, $p );
				}
				if ( '' !== $rel && '/' !== $rel[0] ) {
					return $u; // external, mailto:, tel:
				}
				if ( '' !== $rel ) {
					if ( ! isset( $map['paths'][ $rel ] ) ) {
						return $u; // uploads and other files
					}
					$rel = $map['paths'][ $rel ];
				}
				if ( '' !== $hash && isset( $map['anchors'][ $hash ] ) ) {
					$hash = $map['anchors'][ $hash ];
				}
				return $rel . ( '' !== $hash ? '#' . $hash : '' );
			};
			$cf7_contact = isset( $ids['cf7_contact'] ) ? (int) $ids['cf7_contact'] : 0;
			if ( ! $cf7_contact && class_exists( 'WPCF7_ContactForm' ) ) {
				$src  = WPCF7_ContactForm::get_instance( 505 );
				$mail = $src->prop( 'mail' );
				$mail['body']    = $map['cf7_contact']['mail_body'];
				$mail['subject'] = $map['cf7_contact']['mail_subject'];
				$cf = WPCF7_ContactForm::get_template( array( 'title' => $map['cf7_contact']['title'], 'locale' => 'en_US' ) );
				$cf->set_properties( array(
					'form'     => $map['cf7_contact']['form'],
					'mail'     => $mail,
					'messages' => array_merge( $cf->prop( 'messages' ), $map['cf7_contact']['messages'] ),
				) );
				$cf7_contact = (int) $cf->save();
				$ids['cf7_contact'] = $cf7_contact;
				$say( 'cf7 contact EN: ' . $cf7_contact );
			}
			$menu_slug = 'main-menu-en';
			$menu      = wp_get_nav_menu_object( $menu_slug );
			$menu_id   = $menu ? (int) $menu->term_id : (int) wp_create_nav_menu( 'Main menu (EN)' );
			if ( ! $menu ) {
				wp_update_term( $menu_id, 'nav_menu', array( 'slug' => $menu_slug ) );
			}
			$menu_fr = array( '/en/' => 203, '/en/about/' => 506, '/en/our-services/' => 507, '/en/team/' => 508, '/en/faqs/' => 509, '/en/contact-us/' => 510 );
			$menu_new = array();
			$tr = function ( $node, $key = '' ) use ( &$tr, $map, $url, $cf7_contact, $menu_slug ) {
				if ( is_array( $node ) ) {
					foreach ( $node as $k => $v ) {
						$node[ $k ] = $tr( $v, (string) $k );
					}
					return $node;
				}
				if ( ! is_string( $node ) ) {
					return $node;
				}
				if ( isset( $map['strings'][ $node ] ) ) {
					return str_replace( '__CF7_CONTACT_EN__', (string) $cf7_contact, $map['strings'][ $node ] );
				}
				if ( 'url' === $key ) {
					return $url( $node );
				}
				if ( '_element_id' === $key && isset( $map['anchors'][ $node ] ) ) {
					return $map['anchors'][ $node ];
				}
				if ( 'menu' === $key && 'menu-principal-fr' === $node ) {
					return $menu_slug;
				}
				return $node;
			};
			$copy_meta = array( '_wp_page_template', '_elementor_edit_mode', '_elementor_template_type', '_elementor_version', '_elementor_page_settings' );
			$created   = array();
			foreach ( $map['pages'] as $fr_id => $pg ) {
				$fr_id = (int) $fr_id;
				$en_id = isset( $ids[ $fr_id ] ) ? (int) $ids[ $fr_id ] : 0;
				if ( ! $en_id ) {
					$en_id = wp_insert_post( array(
						'post_type'   => 'page',
						'post_status' => 'publish',
						'post_title'  => $pg['title'],
						'post_name'   => $pg['slug'],
						'menu_order'  => (int) get_post_field( 'menu_order', $fr_id ),
					), true );
					if ( is_wp_error( $en_id ) ) {
						$say( "page $fr_id: " . $en_id->get_error_message() );
						continue;
					}
					$ids[ $fr_id ] = $en_id;
				}
				pll_set_post_language( $en_id, 'en' );
				pll_save_post_translations( array( 'fr' => $fr_id, 'en' => $en_id ) );
				foreach ( $copy_meta as $mk ) {
					$mv = get_post_meta( $fr_id, $mk, true );
					if ( '' !== $mv ) {
						update_post_meta( $en_id, $mk, $mv );
					}
				}
				$data = json_decode( (string) get_post_meta( $fr_id, '_elementor_data', true ), true );
				update_post_meta( $en_id, '_elementor_data', wp_slash( wp_json_encode( $tr( $data ) ) ) );
				$created[ $fr_id ] = array( $en_id, get_post_field( 'post_name', $en_id ), get_permalink( $en_id ) );
			}
			foreach ( (array) wp_get_nav_menu_items( $menu_id ) as $old ) {
				wp_delete_post( $old->ID, true );
			}
			foreach ( $map['menu'] as $i => $it ) {
				$fr = isset( $menu_fr[ $it[1] ] ) ? $menu_fr[ $it[1] ] : 0;
				$pid = ( $fr && ! empty( $ids[ $fr ] ) ) ? (int) $ids[ $fr ] : 0;
				$args = array( 'menu-item-title' => $it[0], 'menu-item-status' => 'publish', 'menu-item-position' => $i + 1 );
				if ( $pid ) {
					$args += array( 'menu-item-type' => 'post_type', 'menu-item-object' => 'page', 'menu-item-object-id' => $pid );
				} else {
					$args += array( 'menu-item-type' => 'custom', 'menu-item-url' => home_url( $it[1] ) );
				}
				$menu_new[] = wp_update_nav_menu_item( $menu_id, 0, $args );
			}
			$say( array( 'menu' => $menu_id, 'items' => $menu_new ) );
			// UAE header and footer: English copies shown on the English pages; the French ones are hidden there.
			$en_pages = array();
			foreach ( $map['pages'] as $fr_id => $pg ) {
				if ( ! empty( $ids[ (int) $fr_id ] ) ) {
					$en_pages[] = 'post-' . (int) $ids[ (int) $fr_id ];
				}
			}
			foreach ( $map['templates'] as $fr_id => $title ) {
				$fr_id = (int) $fr_id;
				$en_id = isset( $ids[ 't' . $fr_id ] ) ? (int) $ids[ 't' . $fr_id ] : 0;
				if ( ! $en_id ) {
					$en_id = wp_insert_post( array( 'post_type' => 'elementor-hf', 'post_status' => 'publish', 'post_title' => $title ), true );
					if ( is_wp_error( $en_id ) ) {
						$say( "template $fr_id: " . $en_id->get_error_message() );
						continue;
					}
					$ids[ 't' . $fr_id ] = $en_id;
				}
				foreach ( array_merge( $copy_meta, array( 'ehf_template_type', 'ehf_target_user_roles' ) ) as $mk ) {
					$mv = get_post_meta( $fr_id, $mk, true );
					if ( '' !== $mv ) {
						update_post_meta( $en_id, $mk, $mv );
					}
				}
				// UAE shows the template whose Polylang language matches the page: both target the entire site.
				update_post_meta( $en_id, 'ehf_target_include_locations', array( 'rule' => array( 'basic-global' ), 'specific' => array() ) );
				update_post_meta( $en_id, 'ehf_target_exclude_locations', array() );
				update_post_meta( $fr_id, 'ehf_target_exclude_locations', array() );
				pll_set_post_language( $fr_id, 'fr' );
				pll_set_post_language( $en_id, 'en' );
				pll_save_post_translations( array( 'fr' => $fr_id, 'en' => $en_id ) );
				$data = $tr( json_decode( (string) get_post_meta( $fr_id, '_elementor_data', true ), true ) );
				if ( 297 === $fr_id ) {
					// The active language is the one drawn in navy: swap the looks of the FR and EN buttons.
					$btns = array();
					$find = function ( &$els ) use ( &$find, &$btns ) {
						foreach ( $els as &$el ) {
							$t = isset( $el['settings']['text'] ) ? $el['settings']['text'] : ( isset( $el['settings']['title'] ) ? $el['settings']['title'] : '' );
							if ( isset( $el['widgetType'] ) && in_array( $t, array( 'FR', 'EN' ), true ) ) {
								$btns[ $t ][] = &$el;
							}
							if ( ! empty( $el['elements'] ) ) {
								$find( $el['elements'] );
							}
						}
					};
					$find( $data );
					$n = min( count( isset( $btns['FR'] ) ? $btns['FR'] : array() ), count( isset( $btns['EN'] ) ? $btns['EN'] : array() ) );
					for ( $i = 0; $i < $n; $i++ ) {
						$a = $btns['FR'][ $i ]['settings'];
						$b = $btns['EN'][ $i ]['settings'];
						$keep = array( 'text', 'title', 'link', '_element_id' );
						$na = $b;
						$nb = $a;
						foreach ( $keep as $kk ) {
							unset( $na[ $kk ], $nb[ $kk ] );
							if ( isset( $a[ $kk ] ) ) {
								$na[ $kk ] = $a[ $kk ];
							}
							if ( isset( $b[ $kk ] ) ) {
								$nb[ $kk ] = $b[ $kk ];
							}
						}
						$btns['FR'][ $i ]['settings'] = $na;
						$btns['EN'][ $i ]['settings'] = $nb;
					}
					$say( "header FR/EN buttons swapped: $n" );
				}
				update_post_meta( $en_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
				$created[ 't' . $fr_id ] = $en_id;
			}
			update_option( 'rcr_en_ids', $ids, false );
			update_option( 'rcr_en_alts', $map['alts'], false );
			if ( class_exists( '\Elementor\Plugin' ) ) {
				\Elementor\Plugin::$instance->files_manager->clear_cache();
			}
			flush_rewrite_rules( false );
			$say( array( 'created' => $created ) );
		}
		if ( 'hf1' === $step ) {
			// UAE asks Polylang (WPML API) for the header/footer in the current language: make them translatable.
			$o = get_option( 'polylang' );
			$o['post_types'] = array_values( array_unique( array_merge( isset( $o['post_types'] ) ? (array) $o['post_types'] : array(), array( 'elementor-hf' ) ) ) );
			update_option( 'polylang', $o );
			$say( array( 'post_types' => $o['post_types'] ) );
		}
		if ( 'hf2' === $step ) {
			$ids = (array) get_option( 'rcr_en_ids', array() );
			foreach ( array( 297, 298 ) as $fr_id ) {
				pll_set_post_language( $fr_id, 'fr' );
				if ( ! empty( $ids[ 't' . $fr_id ] ) ) {
					pll_set_post_language( (int) $ids[ 't' . $fr_id ], 'en' );
					pll_save_post_translations( array( 'fr' => $fr_id, 'en' => (int) $ids[ 't' . $fr_id ] ) );
				}
				// UAE picks the template whose language matches the page, so both can target the entire site.
				update_post_meta( $fr_id, 'ehf_target_exclude_locations', array() );
				if ( ! empty( $ids[ 't' . $fr_id ] ) ) {
					update_post_meta( (int) $ids[ 't' . $fr_id ], 'ehf_target_include_locations', array( 'rule' => array( 'basic-global' ), 'specific' => array() ) );
				}
				$say( $fr_id . ' => ' . wp_json_encode( pll_get_post_translations( $fr_id ) ) );
			}
			if ( isset( $GLOBALS['polylang']->model ) && method_exists( $GLOBALS['polylang']->model, 'clean_languages_cache' ) ) {
				$GLOBALS['polylang']->model->clean_languages_cache();
			}
			delete_transient( 'pll_languages_list' );
			flush_rewrite_rules( false );
			$say( 'en home: ' . pll_home_url( 'en' ) );
		}
		if ( 'front3' === $step ) {
			$res = wp_remote_get( 'https://raw.githubusercontent.com/gajula-atarim/RCR-Rive-Sud/a0ee252013575cdaffc9586f8fc39f6f13c24593/build/mu-plugins/rcr-pll-front.php', array( 'timeout' => 30 ) );
			$php = is_wp_error( $res ) ? '' : wp_remote_retrieve_body( $res );
			if ( 0 !== strpos( $php, '<?php' ) || false === strpos( $php, 'pll_additional_language_data' ) ) {
				throw new Exception( 'mu-plugin not loaded' );
			}
			wp_mkdir_p( WPMU_PLUGIN_DIR );
			file_put_contents( WPMU_PLUGIN_DIR . '/rcr-pll-front.php', $php );
			if ( isset( $GLOBALS['polylang']->model ) && method_exists( $GLOBALS['polylang']->model, 'clean_languages_cache' ) ) {
				$GLOBALS['polylang']->model->clean_languages_cache();
			}
			delete_transient( 'pll_languages_list' );
			$say( 'mu-plugin written: ' . WPMU_PLUGIN_DIR . '/rcr-pll-front.php' );
		}
		if ( 'front4' === $step ) {
			if ( isset( $GLOBALS['polylang']->model ) && method_exists( $GLOBALS['polylang']->model, 'clean_languages_cache' ) ) {
				$GLOBALS['polylang']->model->clean_languages_cache();
			}
			delete_transient( 'pll_languages_list' );
			$en = PLL()->model->get_language( 'en' );
			$say( 'mu filter: ' . ( has_filter( 'pll_additional_language_data' ) ? 'yes' : 'no' ) . ', en page_on_front: ' . ( $en ? $en->page_on_front : '?' ) );
		}
		update_option( 'rcr_i18n_done_' . $step, current_time( 'mysql' ), false );
	} catch ( Throwable $e ) {
		$say( 'ERROR ' . get_class( $e ) . ': ' . $e->getMessage() . ' @' . basename( $e->getFile() ) . ':' . $e->getLine() );
	}
	file_put_contents( $dir . '/log.txt', $step . ' ' . current_time( 'mysql' ) . "\n" . implode( "\n", $log ) . "\n\n", FILE_APPEND );
}, 20 );
