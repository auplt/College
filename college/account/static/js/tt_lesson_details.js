// JS Scripts specially for lesson timetable details template

/* Makes element width the same
 * For class tt_lesson_info_time
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_info_time").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_info_time").css("width", min_width + "px");
});

/* Makes element width the same
 * For class tt_lesson_info_discipline
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_info_discipline").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_info_discipline").css("width", min_width + "px");
});

/* Makes element width the same
 * For class tt_lesson_classroom_name
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_classroom_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".tt_lesson_classroom_name").css("width", min_width + "px");
});

/* Makes element width the same
 * For class info_title
 */
$(document).ready(function () {
  min_width = 0;
  $(".info_title").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });

  if (min_width > 300) {
    min_width = 300;
  }

  $(".info_title").css("width", min_width + "px");
});

/* Makes element width the same
 * For class tt_lesson_date
 */
$(document).ready(function () {
  min_width = 0;
  $(".tt_lesson_date").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });

  if (min_width > 300) {
    min_width = 300;
  }

  $(".tt_lesson_date").css("width", min_width + "px");
});
