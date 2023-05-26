add_video_share_tools = function( me, video ){

	if( video.tagName != 'VIDEO' )
		return;

	$ = jQuery.noConflict( );

	if( $inner = $( video ).parents( '.mejs-video' ) ){

		$video		= $( video );
		$title 		= $video.attr( 'title' );
		share_url	= $video.attr( 'data-url' );
		embed_url	= $video.attr( 'data-url' ); // Change if embed url is different 

		// share urls
		sharelinks = {
			tw: 	'http://twitter.com/share?text=Video: ' + $title + '&url=' + share_url, // twitter
			fb: 	'https://www.facebook.com/sharer/sharer.php?url=' + share_url,	// facebook
			su: 	'http://www.stumbleupon.com/submit?title=' + $title + '&url=' + share_url, //stumble upon
			gp: 	'https://plus.google.com/share?url=' + share_url, //google plus
			em: 	'http://api.addthis.com/oexchange/0.8/forward/email/offer?url=' + share_url, //email
		}

		//create share links
		var links = '';
		for ( var key in sharelinks) {
			links += '<a href="#" rel="nofollow" class="'+key+'">';
		}

		$inner.prepend( '<div class="media-content-title">' + $title + '</div>' );
		$inner.prepend( '<a her="#" rel="nofollow" class="share-video-link">' + 'Share' + '</a>' );

		html  = '<div class="share-video-form">';
		html += '<em class="share-video-close">x</em><h4>' + 'share video' + '</h4>';
		html += '<em>'+ 'link' +'</em><input type="text" class="share-video-lnk share-data" value="' + share_url + '" />' ;

		//embed
		html += '<em>'+ 'embed'  +'</em><textarea class="share-video-embed share-data">';
		html += '&lt;iframe src=&quot;' + embed_url + '&quot; height=&quot;373&quot; width=&quot;640&quot; ';
		html += 'scrolling=&quot;no&quot; frameborder=&quot;0&quot; marginwidth=&quot;0&quot; marginheight=&quot;0&quot;&gt;&lt;/iframe&gt;</textarea>';

		html += '<div class="video-social-share">' + links + '</div>' ;
		$inner.prepend( html + '</div>'  ); 

		// start listeners
		$sharelink 		= $inner.find( '.share-video-link' );
		$sharefrom 	= $inner.find( '.share-video-form' );
		$closelink 		= $inner.find( '.share-video-close' );
		$videotitle	 	= $inner.find( '.media-content-title' );

		// hide form when video is playing
		me.addEventListener( 'play', function(e) {
				$sharelink.hide( ); $sharefrom.hide( ); videotitle.hide( );
		}, false );

		// show form when video is paused
		me.addEventListener( 'pause', function(e) {
				$sharelink.removeClass( 'video-active' );
				$inner.find( '.mejs-overlay-button' ).show( );
				$videotitle.show( ); $sharelink.show( );
		}, false );

		// close video form
		video_close_share_form = function( ){

			$sharefrom.hide( );	
			$sharelink.removeClass( 'video-active' );

			$inner.find( '.mejs-overlay-play' )
			.removeClass( 'share-overlay' );
		};

		// show / hide video form
		$closelink.bind( 'click', video_close_share_form );
		$sharelink.bind( 'click', function( ){

			if( $sharefrom.is( ':hidden' ) ) {

					$sharefrom.show( );
					$sharelink.addClass( 'video-active' );

					$inner.find( '.mejs-overlay-play' )
					.addClass( 'share-overlay' ).show( );

			} else video_close_share_form( );

		});

		// add share links listener
		$inner.find( '.video-social-share a' ).click( function(){
			key = $( this ).attr( 'class' );
			if( sharelinks[key] )
				window.open( sharelinks[key]  );
		});
	}
}