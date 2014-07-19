/*
 *	The following is used on the admin courses page!
 */

$(document).ready(function() {

	/*
	 * Handles the creation of new courses, The data from the course creation
	 * form is retrieved and sent to the server for storage in the datastore.
	 */
	$("#NewCourseForm").submit(function(event) {
		event.preventDefault();

		new_title = $("#CourseTitle").val();
		new_description = $("#CourseDescription").val();
		file = $('#CourseIcon').get(0).files[0];

		var reader = new FileReader();
		var dataURL = null;

		// Closure to capture the file information.
		reader.onload = (function(theFile) {
			return function(e) {
				dataURL = e.target.result;

				$.post("/admin/createcourse", {
					title : new_title,
					description : new_description,
					icon : dataURL,
				}, function(data, status) {
					window.location = "/admin/courses";
				});
			};
		})(file);

		reader.readAsDataURL(file);
	});

	var insideNoClick = false;

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

	/* Delete Course button */
	$(document).on('click', '#deletecoursebtn', function() {

		s_keyid = $(this).parent().parent().attr('keyid');
		alert("deleting!")
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
			alert("text changed!");
			
			// update module
			keyid = $(this).parent().parent().attr('keyid');
			title = $(this).parent().parent().find('h1').text();
			description = $(this).parent().parent().find('p').text();
		} else {
			alert("no change!");
		}

	});

	/* Allow drag and drop */
	$(function() {
		$("#sortable").sortable({
			cancel : "#noDrag",
			stop : function(event, ui) {
				alert("SAVE ORDER!")
			}
		});
	});

});
