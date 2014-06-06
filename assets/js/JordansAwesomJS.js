function showHideToggle(clicked_ID) {
      if (document.getElementById(clicked_ID).innerHTML == "Show Answer") {
            document.getElementById(clicked_ID).innerHTML = "Hide Answer";
      } else {
            document.getElementById(clicked_ID).innerHTML = "Show Answer";
      }

}