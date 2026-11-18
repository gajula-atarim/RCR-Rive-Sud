<?php
/**
 * Plugin Name: RCR Rive-Sud – Polylang front page
 * Description: Makes sure Polylang knows the English home page (/en/) as the English front page.
 *
 * Polylang stores each language's front page in its languages cache. Requests that do not load
 * Polylang's static-page module (REST calls, for example) can build that cache without it, which
 * turns /en/ into /en/home-2/. This fills in the front page from the French home page's translation
 * group, both when the cache is built and every time it is read.
 */

function rcr_pll_front_page_for( $slug ) {
	global $wpdb;
	static $tr = null;
	if ( null === $tr ) {
		$tr    = array();
		$front = 'page' === get_option( 'show_on_front' ) ? (int) get_option( 'page_on_front' ) : 0;
		// Direct query: this can run before the taxonomies are registered.
		$desc = $front ? $wpdb->get_var( $wpdb->prepare(
			"SELECT tt.description FROM {$wpdb->term_relationships} tr INNER JOIN {$wpdb->term_taxonomy} tt ON tt.term_taxonomy_id = tr.term_taxonomy_id WHERE tr.object_id = %d AND tt.taxonomy = 'post_translations' LIMIT 1",
			$front
		) ) : '';
		$val = $desc ? maybe_unserialize( $desc ) : array();
		if ( is_array( $val ) ) {
			$tr = $val;
		}
	}
	return isset( $tr[ $slug ] ) ? (int) $tr[ $slug ] : 0;
}

add_filter( 'pll_additional_language_data', function ( $data, $language ) {
	if ( empty( $data['page_on_front'] ) ) {
		$id = rcr_pll_front_page_for( $language['slug'] );
		if ( $id ) {
			$data['page_on_front'] = $id;
		}
	}
	return $data;
}, 20, 2 );

// Runs every time the list is read from the cache (the hook is deprecated, so silence its notice).
add_filter( 'deprecated_hook_trigger_error', function ( $trigger ) {
	return doing_filter( 'pll_after_languages_cache' ) ? false : $trigger;
} );
add_filter( 'pll_after_languages_cache', function ( $languages ) {
	foreach ( (array) $languages as $lang ) {
		if ( is_object( $lang ) && empty( $lang->page_on_front ) && isset( $lang->slug ) ) {
			$id = rcr_pll_front_page_for( $lang->slug );
			if ( $id ) {
				$lang->page_on_front = $id;
			}
		}
	}
	return $languages;
} );
