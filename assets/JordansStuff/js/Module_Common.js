/*
 * This file contains javascript for the module content navigation menu.
 * 
 * The content navigation menu essentially consists of 3 pages.
 * 
 * 				Modules (choose the module) 
 * 							|
 * 							V
 * 			 Contents (choose the content) 
 * 							| 
 * 							v
 * 			Content_Display (displays chosen content)
 * 
 * 
 * The content navigation menu is implemented in both the admin and normal user
 * part of the site. This file contains c0de that is c0mm0n t0 b0th.
 * 
 */

var insideNoClick = false;

$(document).ready(function() {

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
