
/* Delete content button listener */
$(document).on('click', '.delete-content-button', function() {
	item = $(this).parent().parent().parent();
	item.remove();

});

/* Delete module button listener */
$(document).on('click', '.delete-module-button', function() {
	$(this).parent().parent().parent().parent().remove();
});

$("#savebtn").click(function() {
	alert("saving changes!");

	/* Iterate through every module */
	/* Iterate through the modules contents */

	$("#content-list").children().each(function() {

		modId = $(this).attr('id');

		$(this).children().each(function() {
			$.post("/admin/tutorials", {
				id : modId,
				title : "poop"
			}, function(data, status) {
				alert("Status: " + status);
			});
		});
	});
});

/* Create new form submit function */

$("#NewModuleForm")
		.submit(
				function(event) {
					event.preventDefault();

					new_title = $("#InputTitle").val();
					new_description = $("#InputDescription").val();
					new_icon = $("#InputFile").val();

					// add it to the module list

					$("#sortable")
							.append(
									"<li>" + "<div class=\"topic-info\">"
											+ "<div class=\"row\">"
											+ "<div class=\"col-md-2\">"
											+ "<img src=\""
											+ new_icon
											+ "\" height=\"100\" width=\"100\">"
											+ "</div>"
											+ "<div class=\"col-md-7\">"
											+ "<h1 id=\"noDrag\" contenteditable=\"true\">"
											+ new_title
											+ "</h1>"
											+ "<p id=\"noDrag\" contenteditable=\"true\">"
											+ new_description
											+ "</p>"
											+ "</div>"
											+ "<div class=\"col-md-2\">"
											+ "</div>"
											+ "<div class=\"col-md-1\">"
											+ "<button type=\"button\" id=\"noDrag\" class=\"btn btn-default delete-module-button\">"
											+ "<span class=\"glyphicon glyphicon-remove\"></span>"
											+ "</button>"
											+ "</div>"
											+ "</div>"
											+ "</div>" + "</div>" + "</li>");
					
					
					// reset the form
					$(this)[0].reset();

				});

$(function() {
	$("#sortable").sortable({
		cancel : "#noDrag"
	});
});