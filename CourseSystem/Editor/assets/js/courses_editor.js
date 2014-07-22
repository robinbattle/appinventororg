/*
 *	The following is used on the admin courses editor page!
 *
 *
 *
 *	XXX STATUS: IN PROGRESS
 */

$(document).ready(function() {

	
	
	// if insideNoClick is true the click will not link
	var insideNoClick = false;
	
	// XXX DONE
	/* 
	 * Clickable item boxes that take you to corresponding content page
	 */
	$(document).on('click', '.item-box', function() {
		if (insideNoClick == true) {
			// alert("NO LINK!");
		} else {
			title = $(this).find('h1').text();
			window.location = "courses/" + title;
		}
	});

	
	
	// XXX Done
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

		validated = true;
		errorString = "Missing required fields\n\n";

		if (file == undefined) {
			errorString += "\tYou must select an icon!\n";
			validated = false;
		}

		if (new_title == "") {
			errorString += "\tYou must enter a title!\n";
			validated = false;
		}

		if (validated) {
			reader.readAsDataURL(file);
		} else {
			alert(errorString)
		}
	});

	// XXX DONE
	/* Highlight item boxes on hover */
	$(".item-box").mouseover(function() {
		$(this).addClass('hover');
		$(this).find(".item-box-btns").removeClass('hidden');
	});

	// XXX DONE
	$(".item-box").mouseout(function() {
		$(this).removeClass('hover');
		$(this).find(".item-box-btns").addClass('hidden');
	});

	// XXX DONE
	/* Move module button */
	$(document).on('mouseover', '#movecoursebtn', function() {
		$(this).parent().parent().attr('id', '');
	});

	// XXX DONE
	$(document).on('mouseout', '#movecoursebtn', function() {
		$(this).parent().parent().attr('id', 'noDrag');
	});

	// XXX DONE
	/* Delete Course button */
	$(document).on('click', '#deletecoursebtn', function() {
		s_keyid = $(this).parent().parent().attr('keyid');

		$.post("/admin/deletecourse", {
			keyid : s_keyid
		}, function(data, status) {
			window.location = "/admin/courses";
		});

	});

	// XXX DONE
	/* Prevent certain items from linking to content page on click */
	$(document).on('mouseover', '.noclick', function() {
		insideNoClick = true;
	});

	// XXX DONE
	$(document).on('mouseout', '.noclick', function() {
		insideNoClick = false;
	});

	/* Auto save changes to saveables (title and description) */
	before = "";
	after = "";

	// XXX DONE
	$(document).on('click', '#saveable', function() {
		before = $(this).text();
	});

	// XXX DONE
	$(document).on('blur', '#saveable', function() {
		after = $(this).text();

		
		if (before != after) {
			// update module
			keyid = $(this).parent().parent().attr('keyid');
			title = $(this).parent().parent().find('h1').text();
			description = $(this).parent().parent().find('p').text();
			
			
			// TODO NEED MOAR VALIDATION
			// VALIDATE TITLES SINCE THEY WILL BE USED IN THE URLS
			
			
			if(title == "") {
				alert("title cannot be empty!")
			}
			else {
				
				$.post("/admin/updatecourse", {
					s_keyid : keyid,
					s_title : title,
					s_description : description,
				}, function(data, status) {
					window.location = "/admin/courses";
				});
			}			
		} else {
			// alert("no change!");
		}

	});

	// XXX DONE
	/* Allow drag and drop */
	$(function() {
		$("#sortable").sortable({
			cancel : "#noDrag",
			stop : function(event, ui) {
				saveOrder()
			}
		});
	});

	// XXX DONE
	function saveOrder() {
		var index = -1;
		var resultArray = "";
		$("#sortable").children().each(function() {
			resultArray += ++index + ",";
			resultArray += $(this).attr('keyid') + ",";
		});

		$.post("/admin/updatecourseorder", {
			s_resultArray : resultArray,
		}, function(data, status) {
			window.location = "/admin/courses";
		});
	}
	
	
	// TODO IMPLEMENT ICON CHANGER ON CLICK
	
	// TODO IMPLEMENT CLICK COURSE LINKS TO MODULE EDITOR PAGE
	
});
