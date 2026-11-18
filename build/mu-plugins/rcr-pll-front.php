<?php
/**
 * Plugin Name: RCR Rive-Sud – Polylang front page
 * Description: Keeps the English front page (/en/) in Polylang's languages cache.
 */

/**
 * Polylang caches each language's front page. Requests that do not load Polylang's static-page module
 * (REST calls, for example) can rebuild that cache without it, which turns /en/ into /en/home-2/.
 * Fill it in from the front page's translation group when it is missing.
 */
add_filter( 'pll_additional_language_data', function ( $data, $language ) {
	if ( ! empty( $data['page_on_front'] ) || 'page' !== get_option( 'show_on_front' ) ) {
		return $data;
	}
	global $wpdb;
	$front = (int) get_option( 'page_on_front' );
	// Direct query: this can run before the taxonomies are registered.
	$desc = $front ? $wpdb->get_var( $wpdb->prepare(
		"SELECT tt.description FROM {$wpdb->term_relationships} tr INNER JOIN {$wpdb->term_taxonomy} tt ON tt.term_taxonomy_id = tr.term_taxonomy_id WHERE tr.object_id = %d AND tt.taxonomy = 'post_translations' LIMIT 1",
		$front
	) ) : '';
	$tr = $desc ? maybe_unserialize( $desc ) : array();
	if ( is_array( $tr ) && ! empty( $tr[ $language['slug'] ] ) ) {
		$data['page_on_front'] = (int) $tr[ $language['slug'] ];
	}
	return $data;
}, 20, 2 );
