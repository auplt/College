/* Makes element width the same
 * For class curriculum_discipline_tutor_item_txt
 */
$(document).ready(function () {
  min_width = 0;
  $(".curriculum_discipline_tutor_item_txt").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".curriculum_discipline_tutor_item_txt").css("width", min_width + "px");
});

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

/* Makes element width the same
 * For class semester_number_controller_name
 */
$(document).ready(function () {
  min_width = 0;
  $(".item_semester_number_info_name").each(function () {
    var this_width = $(this)[0].getBoundingClientRect().width;
    if (this_width > min_width) {
      min_width = this_width;
    }
  });
  if (min_width > 300) {
    min_width = 300;
  }
  $(".item_semester_number_info_name").css("width", min_width + "px");
});

/* Collapse all list items except the first one */
$(document).ready(function () {
  $(".semester_number_controller")
    .slice(1, $(".semester_number_controller").length)
    .each(function () {
      // Searching number of elements needed to be hidden
      // let h1 = $(this).parent();

      // while (!h1.is(".item_semester_number")) {
      //   h1 = h1.prev();
      // }
      // let elementsCount = h1.nextUntil(".item_semester_number").length;
      // console.log("elementsCount", elementsCount);

      // let toggleCount = (elementsCount - 1) / 2;

      // let cls = $(this).parent().parent().attr("class");
      // console.log(cls);

      // let toggleElementsCount =
      //   ($("." + cls + " " + ".toggle_name").length > 0) +
      //   ($("." + cls + " " + ".toggle_ctrl").length > 0) +
      //   ($("." + cls + " " + ".toggle_additional").length > 0);
      // console.log(tttt);x

      let toggleNameCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_name").length;
      console.log("toggleNameCount", toggleNameCount);

      let toggleCtrlCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_ctrl").length;
      console.log("toggleCtrlCount", toggleCtrlCount);

      let toggleAdditionalCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_additional").length;
      console.log("toggleAdditionalCount", toggleAdditionalCount);

      let toggleDetailCount = $(this)
        .parent()
        .nextUntil(".item_semester_number")
        .filter(".toggle_detail").length;
      console.log("toggleDetailCount", toggleDetailCount);

      // let toggleCount = (elementsCount - 1) / toggleElementsCount;

      // if ($(".toggle_additional").length) {
      //   toggleCount = (elementsCount - 1) / 3;
      // }

      // console.log(
      //   "toggle_detail",
      //   $(this).parent().parent().find(".toggle_detail"),
      //   $(this).parent().parent().find(".toggle_detail").length
      // );

      // let listElement = $(this).parent().parent();

      // console.log(toggleCount);

      // Hiding found elements when we have toggle details

      // Hidding found elements (group name)
      if (toggleNameCount) {
        $(this)
          .parent()
          .nextAll(".toggle_name")
          .slice(0, toggleNameCount)
          .slideToggle({ duration: 0 });
      }

      // Hidding found elements (delete button)
      if (toggleCtrlCount) {
        $(this)
          .parent()
          .nextAll(".toggle_ctrl")
          .slice(0, toggleCtrlCount)
          .slideToggle({ duration: 0 });
      }

      if (toggleAdditionalCount) {
        $(this)
          .parent()
          .nextAll(".toggle_additional")
          .slice(0, toggleAdditionalCount)
          .slideToggle({ duration: 0 });
      }
      if (toggleDetailCount) {
        $(this)
          .parent()
          .nextAll(".toggle_detail")
          .slice(0, toggleDetailCount)
          .slideToggle({ duration: 0 });
      }
    });
});
