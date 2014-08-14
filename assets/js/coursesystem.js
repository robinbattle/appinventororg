/* The following is used on the courses pages */

// this function is used to translate a title to a url safe title
function wordToPrettyURL(word) {
	urlPrettyTitle = ""
	for(i = 0; i < word.length; i++) {
		if(word.charCodeAt(i) == 32) {
			urlPrettyTitle += '.'
		} else {
			urlPrettyTitle += word[i]
		}
	}
	return urlPrettyTitle;
}


// link to corresponding course page on course-box click
$('.course-box').click(function() {
	window.location = document.URL + "/" + $(this).attr('identifier');
});


//link to corresponding module page on module-box click
$('.module-box').click(function() {
	window.location = document.URL + "/" + wordToPrettyURL($(this).attr('module_title'));
});



//link to corresponding content page on module-box click
$('.content-box').click(function() {
	window.location = document.URL + "/" + wordToPrettyURL($(this).attr('content_title'));
});


//highlight hoverd items in vertical navbar
$('.vertical-content-nav-bar-item, .vertical-content-nav-bar-next-section-box').hover(function() {
	$(this).css('background-color', '#FCFAC7');
}, function() {
	$(this).css('background-color', '');
});

//highlight the content the user is currently on
current_content_title = $('.vertical-content-nav-bar-title').attr('current_content_title');
current_item = $(".vertical-content-nav-bar-item-text:contains('" + current_content_title + "')");
current_item.css('color', '#4F4F4F');
current_item.css('font-weight', '700');


//linkable vertical sidebar items
$('.vertical-content-nav-bar-item').click (function() {
	if($(this).attr('id') == 'modules_page') {
		newUrl = document.URL + "/" + $(this).attr('module_ID') + "/" +$(this).attr('content_ID');
		window.location = newUrl;
	} else {
<<<<<<< HEAD
		window.location = $(this).attr('content_ID');
=======
		alert(wordToPrettyURL($(this).attr('title')));

		window.location = wordToPrettyURL($(this).attr('title'));
>>>>>>> 1110b68198517ee52bcec5e08ad319e48c6249b2
	}
});



$('.vertical-content-nav-bar-next-section-box').click (function() {
	url = String(document.URL).split('/');
	window.location = url[0] + '/' + url[1] + '/' + url[2] + '/' + url[3] + '/' + url[4] + '/' + wordToPrettyURL($(this).attr('title'));
});




// calculate height  of vertical nav bar
$('.vertical-content-nav-bar').css('height', $('body').height() - $('.banner-wrapper').height());


// back to course page button
$('.vertical-content-nav-bar-course-title-text').click(function() {
	url = String(document.URL).split('/');
	
	newURL = ""
	for(i = 0; i < url.length - 2; i++) {
		newURL += url[i] + "/";
	}
	
	newURL += url[i];
	
	window.location = newURL;
});