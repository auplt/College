// JS Scripts specially for group semester form template

/*
 * Adding next group semester to form field
 */
$(document).ready(function () {
  $("#id_group_id").change(function () {
    let url = $(".register_group_semester").attr("data-max-semester");
    let groupId = $(this).val();
    $.ajax({
      url: url,
      data: {
        group_id: groupId,
      },
      success: function (data) {
        $("#id_semester_num").val(data.semester_num__max + 1);
      },
    });
  });
});

/*
 * Adding next group semester to form field
 */
$(document).ready(function () {
  if ($("#id_group_id").val()) {
    let url = $(".register_group_semester").attr("data-max-semester");
    let groupId = $("#id_group_id").val();
    $.ajax({
      url: url,
      data: {
        group_id: groupId,
      },
      success: function (data) {
        $("#id_semester_num").val(data.semester_num__max + 1);
      },
    });
  }
});
