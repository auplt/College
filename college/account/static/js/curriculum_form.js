function deleteItem(element) {
  console.log(element.parent());
  element.parent();
}

$(document).ready(function () {
  $("#discipline_list_add_button").click(function (e) {
    e.preventDefault();
    let url = $(".curriculum_group_form").attr("data-url-img");
    let delete_button = $(
      '<button id="discipline_list_del_button" onclick="return this.parentNode.remove();">' +
        '<img class="del_icon" src="' +
        url +
        '/remove.png" alt="Удалить дисциплину">' +
        "</button>"
    );
    let element = $('<div class="list_item"></div>');
    $("#id_discipline_id").clone().val("").appendTo(element);
    delete_button.appendTo(element);
    element.appendTo(".discipline_list");
  });
});

$(document).ready(function () {
  $("#group_list_add_button").click(function (e) {
    e.preventDefault();
    let url = $(".curriculum_group_form").attr("data-url-img");
    let delete_button = $(
      '<button id="group_list_del_button" onclick="return this.parentNode.remove();">' +
        '<img class="del_icon" src="' +
        url +
        '/remove.png" alt="Удалить группу">' +
        "</button>"
    );
    let element = $('<div class="list_item"></div>');
    $("#id_group_semester_id").clone().val("").appendTo(element);
    delete_button.appendTo(element);
    element.appendTo(".group_list");
  });
});