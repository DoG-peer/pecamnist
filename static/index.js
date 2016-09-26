var odaiList = [
  "",
  "左を向いているすたちゅー",
  "右を向いているすたちゅー",
  "左上を見ているすたちゅー",
  "正面を見ているすたちゅー",
  "背を向けて左を見ているすたちゅー",
  "寝ているすたちゅー",
  "右を見て座っているすたちゅー",
  "背を向けて右を見ているすたちゅー",
  "うどん"
];

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
  manager.nextTask();
  $("#btn_submit").on("click", () => {
    manager.submitData(canvas.convert_320_to_32(),
      () => {
        canvas.clear();
        manager.nextTask();
        manager.nextCount();
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
    this.countView = $("#count");
    this.loadCount();
  }

  loadCount() {
    var n = window.localStorage.getItem('count');
    n = Number(n);
    if (!n) {
      n = 0;
    }
    this.count = n;
    this.updataCountView()
  }
  updataCountView(){
    this.countView.text(this.count);
  }
  nextCount() {
    this.count += 1;
    window.localStorage.setItem('count', this.count);
    this.updataCountView()
  }

  // 新しいお題を始める
  nextTask() {
    this.label = Math.floor(Math.random()*9)+1;
    this.odai.text(odaiList[this.label]);
    this.sample.attr("src", `static/stamp${this.label}.png`);
  }

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
      image: ar,
      label: this.label
    };
    // console.log(JSON.stringify(ar));
    $.ajax({
      type: 'POST',
      url: 'api/items',
      dataType: 'json',
      contentType:'application/json',
      data: JSON.stringify(data),
      success: (mes) => {
        console.log("success");
        console.log(mes);
        f();
      },
      error: (e) => {
        console.log("error");
        console.log(e);
      }
    });
  }
}

