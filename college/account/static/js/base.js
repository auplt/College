$(document).ready(function () {
  $(".msg_cross").click(function () {
    $(this).parent().hide();
  });
});

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

// $(document).ready(function () {
//   let input = $("input");
//   for (i = 0; i < input.length; i++) {
//     console.log(input[i]);
//     console.log(input[i].hasAttribute("placeholder"));
//     if (input[i].hasAttribute("placeholder") && input[i].value === "") {
//       var this_width = input[i].getAttribute("placeholder").width;
//       console.log(this_width);

//       // input[i].setAttribute(
//       //   "size",
//       //   input[i].getAttribute("placeholder").length - 1
//       // );
//       // console.log(input[i].getAttribute("placeholder").length);
//     }
//   }
// });
