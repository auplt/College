// JS Scripts for all templates

/*
 * Closes pop-up message on cross click
 */
$(document).ready(function () {
  $(".msg_cross").click(function () {
    $(this).parent().hide();
  });
});

/* Makes element width the same
 * For class item_title_heading
 */
$(document).ready(function () {
  min_width = 0;
  $(".items_list .items_list_sem_items .item_title .item_title_heading").each(
    function () {
      var this_width = $(this)[0].getBoundingClientRect().width;
      if (this_width > min_width) {
        min_width = this_width;
      }
    }
  );
  if (min_width > 300) {
    min_width = 300;
  }
  $(".items_list .items_list_sem_items .item_title").css(
    "width",
    min_width + "px"
  );
});
