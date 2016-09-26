$(() => {
  var painter = new Painter();
  var canvas = new Canvas("main_canvas", painter);
  var pen = new Pen("pen", {
    mousedown: e => {
      var pos = canvas.position(e);
      pen.x = pos[0];
      pen.y = pos[1];
      pen.isDrawing = true;
      canvas.drawPoint(pos[0], pos[1]);
    },
    mousemove: e => {
      if (!pen.isDrawing) return;
      var pos = canvas.position(e);
      canvas.drawLine(pen.x, pen.y, pos[0], pos[1]);
      pen.x = pos[0];
      pen.y = pos[1];
    },
    mouseup: e => {
      pen.isDrawing = false;
    },
    mouseleave: e => {
      pen.isDrawing = false;
    }
  });

  var eraser = new Pen("eraser", {
    mousedown: e => {
      var pos = canvas.position(e);
      eraser.x = pos[0];
      eraser.y = pos[1];
      eraser.isDrawing = true;
      canvas.drawPoint(pos[0], pos[1], 5, "rgba(255, 255, 255, 1)");
    },
    mousemove: e => {
      if (!eraser.isDrawing) return;
      var pos = canvas.position(e);
      canvas.drawLine(eraser.x, eraser.y, pos[0], pos[1], 5, "rgba(255, 255, 255, 1)");
    },
    mouseup: e=> {
      eraser.isDrawing = false;
    },
    mouseleave: e=> {
      eraser.isDrawing = false;
    }
  });
  painter.use(pen);
  new ToolButton("btn_pen", pen, painter);
  new ToolButton("btn_eraser", eraser, painter);
  $("#btn_clear").on("click", () => {
    canvas.clear();
  });

  var manager = new Manager();
  // manager.nextTask();
  $("#btn_submit").on("click", () => {
    manager.submitData(canvas.convert_320_to_32(),
      () => {
        // canvas.clear();
        // manager.nextTask();
      }
    );
  });

  var can2 = new Canvas("preview_canvas", new Painter());
  setInterval(() => {
    var img2 = canvas.convert_320_to_32();
    can2.context.putImageData(img2, 0, 0);
  }, 1000);
});

class Manager{
  constructor(){
    this.odai = $("#odai");
    this.sample = $("#sample");
    this.result = $("#result");
    this.ai_select = $("#select_ai");
    this.result_labels = [];
    for(var i=1; i<10; i++){
      this.result_labels.push($(`#result${i}`));
    }
  }
  /*
  // 新しいお題を始める
  nextTask() {
    this.label = Math.floor(Math.random()*9)+1;
    this.odai.text("すた#" + this.label);
    this.sample.attr("src", `static/stamp${this.label}.png`);
  }
  */
  // 32*32個の数値の列が送られる
  submitData(data, f){
    var ar = [];
    var isWhite = true;
    for(var i=0; i<32*32; i++) {
      var mean = 0;
      for(var j=0; j<3; j++){
        mean += data.data[i*4+j];
      }
      mean /= 3;
      if(mean<255){
        isWhite = false;
      }
      ar.push(mean);
    }
    if(isWhite){
      alert("なんか書いてね！");
      return;
    }

    var data = {
      ai_name: this.ai_select.val(),
      image: ar
    };
    var that = this;
    // console.log(JSON.stringify(ar));
    $.ajax({
      type: "POST",
      url: "api/ai/infer",
      dataType: 'json',
      contentType:'application/json',
      data: JSON.stringify(data),
      success: (mes) => {
        console.log("success");
        console.log(mes);
        that.show(mes.data);
        f();
      },
      error: (e) => {
        console.log("error");
        console.log(e);
      }
    });
  }
  show(data){
    for(var i=0; i<9;i++){
      this.result_labels[i].text((data[i]*100).toFixed(2))
    }
  }
}

