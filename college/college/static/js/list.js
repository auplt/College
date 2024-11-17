// JS Scripts for toggle lists

/* Function that calculates element angle in degrees */
function getDegreeElementById(element) {
  let style = window.getComputedStyle(element, null);
  // Recieving styles values
  let valueStyle =
    style.getPropertyValue("-webkit-transform") ||
    style.getPropertyValue("-moz-transform") ||
    style.getPropertyValue("-ms-transform") ||
    style.getPropertyValue("-o-transform") ||
    style.getPropertyValue("transform");
  // If there is no attribute than angle equals 0 degree
  if (valueStyle == "none") return 0;
  // Splitting received value
  let values = valueStyle.split("(")[1];
  values = values.split(")")[0];
  values = values.split(",");
  // СCalculation sin and cos
  let cos = values[0];
  let sin = values[1];
  // Calculating angle
  let degree = Math.round(Math.asin(sin) * (180 / Math.PI));
  if (cos < 0) {
    addDegree = 90 - Math.round(Math.asin(sin) * (180 / Math.PI));
    degree = 90 + addDegree;
  }
  if (degree < 0) {
    degree = 360 + degree;
  }
  return degree;
}

/* Function for rotating element */
jQuery.fn.rotate = function (degrees) {
  $(this).css({
    "-webkit-transform": "rotate(" + degrees + "deg)",
    "-moz-transform": "rotate(" + degrees + "deg)",
    "-ms-transform": "rotate(" + degrees + "deg)",
    transform: "rotate(" + degrees + "deg)",
  });
  return $(this);
};

/* Initial element rotation */
$(".semester_number_controller").first().rotate(90);
$(".group_info_curriculum .semester_number_controller").first().rotate(90);
$(document).ready(function () {
  $(".semester_number_controller").first().rotate(90);
  $(".group_info_curriculum .semester_number_controller").first().rotate(90);
});

/* Function for elements toggling */
$(document).ready(function () {
  $(".semester_number_controller").click(function () {
    let toggleNameCount = $(this)
      .parent()
      .nextUntil(".item_semester_number")
      .filter(".toggle_name").length;

    let toggleCtrlCount = $(this)
      .parent()
      .nextUntil(".item_semester_number")
      .filter(".toggle_ctrl").length;

    let toggleAdditionalCount = $(this)
      .parent()
      .nextUntil(".item_semester_number")
      .filter(".toggle_additional").length;

    let toggleDetailCount = $(this)
      .parent()
      .nextUntil(".item_semester_number")
      .filter(".toggle_detail").length;

    // Hidding found elements (group name)
    if (toggleNameCount) {
      $(this)
        .parent()
        .nextAll(".toggle_name")
        .slice(0, toggleNameCount)
        .slideToggle("slow");
    }

    // Hidding found elements (delete button)
    if (toggleCtrlCount) {
      $(this)
        .parent()
        .nextAll(".toggle_ctrl")
        .slice(0, toggleCtrlCount)
        .slideToggle("slow");
    }

    if (toggleAdditionalCount) {
      $(this)
        .parent()
        .nextAll(".toggle_additional")
        .slice(0, toggleAdditionalCount)
        .slideToggle("slow");
    }
    if (toggleDetailCount) {
      $(this)
        .parent()
        .nextAll(".toggle_detail")
        .slice(0, toggleDetailCount)
        .slideToggle("slow");
    }

    // Prevents multiple animation
    time = 0;
    // Rotating arrow on open/close list
    $(this).animate(
      { textIndent: 0 },
      {
        step: function () {
          if (time == 0) {
            if (getDegreeElementById(this) == 0) {
              $(this).rotate(90);
            } else {
              $(this).rotate(0);
            }
            time += 1;
          }
        },
        duration: "slow",
      },
      "linear"
    );
  });
});
