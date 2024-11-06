// JS Scripts specially for group details template

/* Makes element width the same
 * For class curriculum_discipline
 */
$(document).ready(function () {
  min_width = 0;
  $(".curriculum_discipline").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });

  if (min_width > 300) {
    min_width = 300;
  }

  $(".curriculum_discipline").css("width", min_width + "px");
});
