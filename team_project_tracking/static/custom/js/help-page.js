//
// 	JQUERY DEPENDENCY
//
//
// <script type="text/javascript" async="" src="https://ssl.google-analytics.com/ga.js"></script>
// <script src="../jquery-v1.min.js"></script>

	// 'use strict';


	// search & highlight

	;( function( $, window, document, undefined )
	{
		var $container = $( '.faq' );
		if( !$container.length ) return true;

		var $input			= $container.find( 'input' ),
			$notfound		= $container.find( '.faq__notfound' ),
			$items			= $container.find( '> ul > li' ),
			$item			= $(),
			itemsIndexed	= [];

		$items.each( function()
		{
			itemsIndexed.push( $( this ).text().replace( /\s{2,}/g, ' ' ).toLowerCase() );
		});

		$input.on( 'keyup', function( e )
		{
			if( e.keyCode == 13 ) // enter
			{
				$input.trigger( 'blur' );
				return true;
			}

			$items.each( function()
			{
				$item = $( this );
				$item.html( $item.html().replace( /<span class="highlight">([^<]+)<\/span>/gi, '$1' ) );
			});

			var searchVal = $.trim( $input.val() ).toLowerCase();
			if( searchVal.length )
			{
				for( var i in itemsIndexed )
				{
					$item = $items.eq( i );
					if( itemsIndexed[ i ].indexOf( searchVal ) != -1 )
						$item.removeClass( 'is-hidden' ).html( $item.html().replace( new RegExp( searchVal+'(?!([^<]+)?>)', 'gi' ), '<span class="highlight">$&</span>' ) );
					else
						$item.addClass( 'is-hidden' );
				}
			}
			else $items.removeClass( 'is-hidden' );

			$notfound.toggleClass( 'is-visible', $items.not( '.is-hidden' ).length == 0 );
		});
	})( jQuery, window, document );


	// toggling items on title press

	;( function( $, window, document, undefined )
	{
		$( document ).on( 'click', '.faq h2 a', function( e )
		{
			e.preventDefault();
			$( this ).parents( 'li' ).toggleClass( 'is-active' );
		});
	})( jQuery, window, document );


	// auto-show item content when show results reduces to single

	;( function( $, window, document, undefined )
	{
		var $container = $( '.faq' );
		if( !$container.length ) return true;

		var $input		= $container.find( 'input' ),
			$items		= $container.find( '> ul > li' ),
			$item		= $();

		$input.on( 'keyup', function()
		{
			$item = $items.not( '.is-hidden' );
			if( $item.length == 1 )
				$item.addClass( 'js--autoshown is-active' );
			else
				$items.filter( '.js--autoshown' ).removeClass( 'js--autoshown is-active' );
		});
	})( jQuery, window, document );


/*

	NO DEPENDENCIES (IE9+ support)

<script>

	'use strict';

	;( function ( document, window, index )
	{
		var hasElementClass		= function( element, className ){ return element.classList ? element.classList.contains( className ) : new RegExp( '(^| )' + className + '( |$)', 'gi' ).test( element.className ); },
			addElementClass		= function( element, className ){ element.classList ? element.classList.add( className ) : element.className += ' ' + className; },
			removeElementClass	= function( element, className ){ element.classList ? element.classList.remove( className ) : element.className = element.className.replace( new RegExp( '(^|\\b)' + className.split( ' ' ).join( '|' ) + '(\\b|$)', 'gi' ), ' ' ); };


		// search & highlight

		;( function ( document, window, index )
		{
			var container = document.querySelector( '.faq' );
			if( !container ) return true;

			var input			= container.querySelector( 'input' ),
				notfound		= container.querySelector( '.faq__notfound' ),
				items			= document.querySelectorAll( '.faq > ul > li' ),
				item			= {},
				itemsIndexed	= [];

			[].forEach.call( items, function( entry )
			{
				itemsIndexed.push( entry.textContent.replace( /\s{2,}/g, ' ' ).toLowerCase() );
			});

			input.addEventListener( 'keyup', function( e )
			{
				if( e.keyCode == 13 ) // enter
				{
					input.blur();
					return true;
				}

				[].forEach.call( items, function( entry )
				{
					entry.innerHTML = entry.innerHTML.replace( /<span class="highlight">([^<]+)<\/span>/gi, '$1' );
				});

				var searchVal = input.value.trim().toLowerCase();
				if( searchVal.length )
				{
					itemsIndexed.forEach( function( entry, i )
					{
						if( itemsIndexed[ i ].indexOf( searchVal ) != -1 )
						{
							removeElementClass( items[ i ], 'is-hidden' );
							items[ i ].innerHTML = items[ i ].innerHTML.replace( new RegExp( searchVal+'(?!([^<]+)?>)', 'gi' ), '<span class="highlight">$&</span>' );
						}
						else
							addElementClass( items[ i ], 'is-hidden' );
					});
				}
				else [].forEach.call( items, function( entry ){ removeElementClass( entry, 'is-hidden' ); });

				if( items.length == [].filter.call( items, function( entry ){ return hasElementClass( entry, 'is-hidden' ) } ).length )
					addElementClass( notfound, 'is-visible' );
				else
					removeElementClass( notfound, 'is-visible' );

			});
		}( document, window, 0 ));


		// toggling items on title press

		;( function ( document, window, index )
		{
			[].forEach.call( document.querySelectorAll( '.faq h2 a' ), function( entry )
			{
				addElementClass( entry, 'js--is-toggleable-item' );
			});

			document.addEventListener( 'click', function( e )
			{
				if( hasElementClass( e.target, 'js--is-toggleable-item' ) )
				{
					e.preventDefault();
					var current = e.target;
					while( current.parentNode )
					{
						current = current.parentNode;
						if( current.tagName.toLowerCase() == 'li' )
						{
							hasElementClass( current, 'is-active' ) ? removeElementClass( current, 'is-active' ) : addElementClass( current, 'is-active' );
							break;
						}
					}
				}
			});
		}( document, window, 0 ));


		// auto-show item content when show results reduces to single

		;( function ( document, window, index )
		{
			var container = document.querySelector( '.faq' );
			if( !container ) return true;

			var input	= container.querySelector( 'input' ),
				items	= document.querySelectorAll( '.faq > ul > li' ),
				item	= {};

			input.addEventListener( 'keyup', function( e )
			{
				item = [].filter.call( items, function( entry ){ return !hasElementClass( entry, 'is-hidden' ); } )

				if( item.length == 1 )
				{
					addElementClass( item[ 0 ], 'js--autoshown' );
					addElementClass( item[ 0 ], 'is-active' );
				}
				else
					[].forEach.call( items, function( entry )
					{
						if( hasElementClass( entry, 'js--autoshown' ) )
						{
							removeElementClass( entry, 'js--autoshown' );
							removeElementClass( entry, 'is-active' );
						}
					});
			});
		}( document, window, 0 ));

	}( document, window, 0 ));

</script>

*/
