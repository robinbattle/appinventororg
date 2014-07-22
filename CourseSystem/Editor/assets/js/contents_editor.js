/*
 *	The following is used on the contents editor page! 
 * 
 * 
 */

/**
 * Retrieves data from the new content form, and then submits it to the server.
 */

$("#NewContentForm").submit(function(event) {
	event.preventDefault();
	
	title = $("#ContentTitle").val();
	description = $("#ContentDescription").val();
	target = $("#ContentURL").val();
	content_type = $('input:radio[name=inlineRadioOptions]:checked').val();
	course_id = $('.subject-box-top-half-inner').attr('course_id')
	module_id = $('.subject-box-top-half-inner').attr('module_id')

	
	
	validated = true;
	errorString = "Missing required fields\n\n";

	if (title == "") {
		errorString += "\tYou must enter a title!\n";
		validated = false;
	}
	
	if (target == "") {
		errorString += "\tYou must enter a url!\n";
		validated = false;
	}
	
	if (content_type == undefined) {
		errorString += "\tYou must choose a type!\n";
		validated = false;
	}


	if (validated) {
		// submit it!
		$.post("/admin/course_system/create/Content", {
			s_title : title,
			s_description : description,
			s_target : target,
			s_content_type : content_type,
			s_course_id : course_id,
			s_module_id : module_id
		}, function(data, status) {
			location.reload()
		});
	} else {
		alert(errorString)
	}
	
});

$(document).ready(function() {

	// true if mouseover noclick element, false otherwise
	var insideNoClick = false;

	/* Clickable item boxes that take you to corresponding content page */
	$(document).on('click', '.item-box', function() {
		if (insideNoClick == true) {
			// alert("NO LINK!");
		} else {
			window.location = "http://" + $(this).attr('href');
		}
	});

	/* Highlight item boxes on hover */
	$(".item-box").mouseover(function() {
		$(this).addClass('hover');
		$(this).find(".module-btns").removeClass('hidden');
	});

	$(".item-box").mouseout(function() {
		$(this).removeClass('hover');
		$(this).find(".module-btns").addClass('hidden');
	});

	/* Delete content button */
	$(document).on('click', '#deletemodulebtn', function() {
		s_content_id = $(this).parent().parent().attr('keyid');
		s_module_id = $('.subject-box-top-half-inner').attr("module_id")
		s_course_id = $('.subject-box-top-half-inner').attr("course_id")
		
		$.post("/admin/course_system/delete/Content", {
			content_id : s_content_id,
			module_id : s_module_id,
			course_id : s_course_id
		}, function(data, status) {
			location.reload(true)
			
		});
	});

	/* Auto save changes to saveables (title and description) */
	before = "";
	after = "";

	$(document).on('click', '#saveable', function() {
		before = $(this).text();
	});

	$(document).on('blur', '#saveable', function() {
		after = $(this).text();

		if (before != after) {
			// update module
			content_keyid = $(this).parent().parent().attr('keyid');
			title = $(this).parent().parent().find('h1').text();
			description = $(this).parent().parent().find('p').text();
			module_keyid = $("#idholder").attr('keyid');

			$.post("/admin/updatecontent", {
				s_content_keyid : content_keyid,
				s_module_keyid : module_keyid,
				s_title : title,
				s_description : description,
			}, function(data, status) {
				window.location = "/admin/content?keyid=" + module_keyid;
			});

		} else {
			// alert("no change!");
		}

	});

	/* Allow drag and drop */
	$(function() {
		$("#sortable").sortable({
			cancel : "#noDrag",
			stop : function(event, ui) {
				saveOrder();

			}
		});
	});

	function saveOrder() {
		var index = -1;
		var resultArray = "";
		var mod_keyid = $("#idholder").attr('keyid');
		$("#sortable").children().each(function() {
			resultArray += ++index + ",";
			resultArray += $(this).attr('keyid') + ",";
		});

		$.post("/admin/updatecontentorder", {
			s_mod_keyid : mod_keyid,
			s_resultArray : resultArray,
		}, function(data, status) {
			window.location = "/admin/content?keyid=" + mod_keyid;
		});

	}

	/* Move module button */
	$(document).on('mouseover', '#movemodulebtn', function() {
		$(this).parent().parent().attr('id', '');
	});

	$(document).on('mouseout', '#movemodulebtn', function() {
		$(this).parent().parent().attr('id', 'noDrag');
	});

	/* Prevent certain items from linking to content page on click */
	$(document).on('mouseover', '.noclick', function() {
		insideNoClick = true;
	});

	$(document).on('mouseout', '.noclick', function() {
		insideNoClick = false;
	});
});