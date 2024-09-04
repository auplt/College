$(document).ready(function () {
$("#id_group_id").change(function() {
    let url = $(".register_group_semester").attr("data-max-semester");
    console.log(url);
    let groupId = $(this).val();
    console.log(groupId);
    $.ajax({
    url:url,
    data: {
    'group_id' : groupId},
    success: function (data) {
        $("#id_semester_num").val(data.semester_num__max + 1);
    }
    });

});
});

$(document).ready(function () {
if ($("#id_group_id").val()){
    console.log($("#id_group_id").val());
    console.log("second");
    let url = $(".register_group_semester").attr("data-max-semester");
    console.log(url);
    let groupId = $("#id_group_id").val();
    console.log(groupId);
    $.ajax({
    url:url,
    data: {
    'group_id' : groupId},
    success: function (data) {
        $("#id_semester_num").val(data.semester_num__max + 1);
    }
    });
    }


})