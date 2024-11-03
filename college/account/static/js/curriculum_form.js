// JS Scripts specially for curriculum form template

/*
 * Function for deleting additional form field
 */
function deleteItem(element) {
  element.parent();
}

/*
 * Function for dadding new additional field for discipline information
 */
$(document).ready(function () {
  $("#discipline_list_add_button").click(function (e) {
    e.preventDefault();
    let url = $(".curriculum_group_form").attr("data-url-img");
    let delete_button = $(
      '<button class="del_button" id="discipline_list_del_button" onclick="return this.parentNode.remove();">' +
        '<img class="del_icon" src="' +
        url +
        '/trash.svg" alt="Удалить дисциплину">' +
        "</button>"
    );
    let element = $('<div class="list_item"></div>');
    $("#id_discipline_id").clone().val("").appendTo(element);
    delete_button.appendTo(element);
    element.appendTo(".discipline_list");
  });
});

/*
 * Function for dadding new additional field for group information
 */
$(document).ready(function () {
  $("#group_list_add_button").click(function (e) {
    e.preventDefault();
    let url = $(".curriculum_group_form").attr("data-url-img");
    let delete_button = $(
      '<button class="del_button" id="group_list_del_button" onclick="return this.parentNode.remove();">' +
        '<img class="del_icon" src="' +
        url +
        '/trash.svg" alt="Удалить группу">' +
        "</button>"
    );
    let element = $('<div class="list_item"></div>');
    $("#id_group_semester_id").clone().val("").appendTo(element);
    delete_button.appendTo(element);
    element.appendTo(".group_list");
  });
});
