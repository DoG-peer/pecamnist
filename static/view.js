var view;
$(() => {
  view = new View("view_canvas");
  $.ajax({
    type: 'GET',
    url: `/api/items/${view.key}`,
    dataType: 'json',
    contentType: 'application/json',
    success: (data) => {
      console.log(data);
      view.show(data["image"], data["label"]);
    },
    error: (e) => {
      console.log("error");
      console.log(e);
    }
  })
});

class View {
  constructor(id){
    this.canvas = new Canvas(id, new Painter());
    this.key = parseInt($("#id").text(), 10);
  }
  show(data, label){
    this.canvas.showGray(data, 10);
    $("#label").text(label);
    $("#sample_image").attr("src", `/static/stamp${label}.png`);
  }
}
