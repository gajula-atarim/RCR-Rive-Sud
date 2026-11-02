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
