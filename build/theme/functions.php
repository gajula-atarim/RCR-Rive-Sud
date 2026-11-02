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
 * TEMPORARY one-time importer for the Elementor layouts (Home, UAE header, UAE footer).
 * Reads rcr-import/*.json from this theme, writes them as Elementor data, then does nothing
 * until the file changes. Remove this block and the rcr-import folder once the build is final.
 */
add_action( 'wp_loaded', function () {
	$dir = get_stylesheet_directory() . '/rcr-import/';
	$map = array(
		15 => 'home.json',
		16 => 'header.json',
		17 => 'footer.json',
	);
	$changed = false;
	foreach ( $map as $post_id => $file ) {
		$path = $dir . $file;
		if ( ! file_exists( $path ) || ! get_post( $post_id ) ) {
			continue;
		}
		$json = file_get_contents( $path );
		$hash = md5( $json );
		if ( get_post_meta( $post_id, '_rcr_import_hash', true ) === $hash ) {
			continue;
		}
		$data = json_decode( $json, true );
		if ( ! is_array( $data ) || empty( $data ) ) {
			continue;
		}
		update_post_meta( $post_id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
		update_post_meta( $post_id, '_elementor_edit_mode', 'builder' );
		if ( defined( 'ELEMENTOR_VERSION' ) ) {
			update_post_meta( $post_id, '_elementor_version', ELEMENTOR_VERSION );
		}
		delete_post_meta( $post_id, '_elementor_css' );
		delete_post_meta( $post_id, '_elementor_element_cache' );
		delete_post_meta( $post_id, '_elementor_page_assets' );
		update_post_meta( $post_id, '_rcr_import_hash', $hash );
		$changed = true;
	}
	if ( $changed && class_exists( '\Elementor\Plugin' ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
}, 99 );
