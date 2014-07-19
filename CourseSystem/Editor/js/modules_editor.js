/**
 * The following is used on the Admin Modules page!
 */

/**
 * Retrieves data from the new content form, and then submits it to the server.
 */


/**
 * Retrieves data from new module form, validates it, and then submits it the
 * server.
 */
$("#NewModuleForm").submit(function(event) {
	event.preventDefault();

	new_title = $("#ModuleTitle").val();
	new_description = $("#ModuleDescription").val();
	file = $('#ModuleIcon').get(0).files[0];

	var reader = new FileReader();
	var dataURL = null;

	// Closure to capture the file information.
	reader.onload = (function(theFile) {
		return function(e) {
			dataURL = e.target.result;

			$.post("/admin/createmodule", {
				title : new_title,
				description : new_description,
				icon : dataURL,
			}, function(data, status) {
				window.location = "/admin/modules";
			});
		};
	})(file);

	reader.readAsDataURL(file);
});

$(document).ready(function() {

	var insideNoClick = false;

	/* Clickable item boxes that take you to corresponding content page */
	$(document).on('click', '.item-box', function() {
		if (insideNoClick == true) {
			// alert("NO LINK!");
		} else {
			window.location = "/admin/content?keyid=" + $(this).attr('keyid');

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

	/* Move module button */
	$(document).on('mouseover', '#movemodulebtn', function() {
		$(this).parent().parent().attr('id', '');
	});

	$(document).on('mouseout', '#movemodulebtn', function() {
		$(this).parent().parent().attr('id', 'noDrag');
	});

	/* Delete module button */
	$(document).on('click', '#deletemodulebtn', function() {

		s_keyid = $(this).parent().parent().attr('keyid');

		$.post("/admin/deletemodule", {
			keyid : s_keyid
		}, function(data, status) {
			window.location = "/admin/modules";
		});
	});

	/* Prevent certain items from linking to content page on click */
	$(document).on('mouseover', '.noclick', function() {
		insideNoClick = true;
	});

	$(document).on('mouseout', '.noclick', function() {
		insideNoClick = false;
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
			// alert("text changed!");

			// update module
			keyid = $(this).parent().parent().attr('keyid');
			title = $(this).parent().parent().find('h1').text();
			description = $(this).parent().parent().find('p').text();

			$.post("/admin/updatemodule", {
				s_title : title,
				s_description : description,
				s_keyid : keyid,
			}, function(data, status) {
				window.location = "/admin/modules";
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
		$("#sortable").children().each(function() {
			resultArray += ++index + ",";
			resultArray += $(this).attr('keyid') + ",";
		});

		$.post("/admin/updatemoduleorder", {
			s_array : resultArray,
		}, function(data, status) {
			window.location = "/admin/modules";
		});

	}

});
