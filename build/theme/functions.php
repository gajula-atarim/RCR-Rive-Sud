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
 * French home page (/fr/): declare the page language as French (fr-CA) so browsers,
 * screen readers and search engines read it correctly, and add an "rcr-lang-fr" body class
 * used by style.css for French typography rules.
 */
function rcr_is_french_page() {
	return is_page( 'fr' );
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
 * TEMPORARY one-shot importer for the 7 Nov 2026 update (removed right after it runs).
 * Loads the generated Elementor JSON for the home page (203) and the new pages (380, 381, 382).
 * The current home page data is backed up first in the option rcr_backup_203_nov7.
 */
add_action( 'init', function () {
	if ( get_option( 'rcr_import_nov7_done' ) || ! isset( $_GET['rcr_import_nov7'] ) ) {
		return;
	}
	$base = 'https://raw.githubusercontent.com/gajula-atarim/RCR-Rive-Sud/86d936a2a6c78fa19630fad57c6a35d77f9eb657/build/elementor/out/';
	$map  = array( 203 => 'home_fr', 380 => 'page_cardio_secours', 381 => 'page_sir', 382 => 'page_confidentialite' );
	$data = array();
	foreach ( $map as $id => $file ) {
		$res = wp_remote_get( $base . $file . '.json', array( 'timeout' => 30 ) );
		$body = is_wp_error( $res ) ? '' : wp_remote_retrieve_body( $res );
		$tree = json_decode( $body, true );
		if ( ! is_array( $tree ) || empty( $tree ) ) {
			update_option( 'rcr_import_nov7_error', $file, false );
			return; // nothing is written unless every file loaded
		}
		$data[ $id ] = wp_json_encode( $tree );
	}
	add_option( 'rcr_backup_203_nov7', get_post_meta( 203, '_elementor_data', true ), '', false );
	foreach ( $data as $id => $json ) {
		update_post_meta( $id, '_elementor_data', wp_slash( $json ) );
		update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	}
	if ( class_exists( '\Elementor\Plugin' ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
	update_option( 'rcr_import_nov7_done', current_time( 'mysql' ), false );
}, 20 );
