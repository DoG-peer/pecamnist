class Canvas {
  constructor(id, painter, scale=1) {
    this.id = id;
    this.painter = painter;
    this.scale = scale;
    this.canvas = document.getElementById(id);
    this.context = this.canvas.getContext("2d");
    this.context.scale(scale, scale);
    this.borderWidth = 0;
    this.pen = true;
    this.width = parseInt($("#" + id).css("width"));
    this.height = parseInt($("#" + id).css("height"));
    this.setActions();
    this.clear();
  }

  position(e) {
    var x = e.pageX - $("#" + this.id).offset().left - this.borderWidth;
    var y = e.pageY - $("#" + this.id).offset().top - this.borderWidth;
    return [x/this.scale, y/this.scale];
  }

  clear() {
    var color = "#FFFFFF";
    this.context.strokeStyle = color;
    this.context.fillStyle = color;
    this.context.beginPath();
    this.context.fillRect(0, 0, this.width, this.height);
    this.context.fill();
    this.context.stroke();
    //this.context.clearRect(0, 0, this.width, this.height);
  }
  setActions(painter = this.painter) {
    ["mousedown", "mousemove", "mouseup", "mouseleave"].forEach(actionName=> {
      this.resetAction(actionName);
      this.setAction(actionName, painter);
    });
  }
  setAction(actionName, painter= this.painter) {
    $("#" + this.id).on(actionName, e => {
      if (painter.tool && painter.tool.actions[actionName]) {
        painter.tool.actions[actionName](e);
      }
    });
  }
  resetAction(actionName) {
    $("#" + this.id).on(actionName, e => { });
  }

  drawPoint(x, y, width=3, color="#000000") {
    this.context.strokeStyle = color;
    this.context.fillStyle = color;
    this.context.beginPath();
    this.context.arc(x, y, width / 2, 0, Math.PI * 2, false);
    this.context.fill();
  }

  drawLine(x, y, xx, yy, width=3, color="#000000") {
    this.context.strokeStyle = color;
    this.context.fillStyle = color;
    this.context.lineWidth = width;
    this.context.beginPath();
    this.context.moveTo(x, y);
    this.context.lineTo(xx, yy);
    this.context.stroke();

  }

  convert_320_to_32() {
    var img = this.context.getImageData(0, 0, 320, 320);
    var img2 = new ImageData(32, 32);
    for(var i=0; i<32; i++){
      for(var j=0; j<32; j++){
        for(var k=0; k<4; k++){
          var val = 0;
          for(var p=0; p<10;p++){
            for(var q=0; q<10;q++){
              val += 255 - img.data[320*4*(10*i+p) + (10*j + q)*4 + k];

            }
          }
          img2.data[32*4*i+j*4+k] = 255 - val/30;
        }
      }
    }
    return img2;
  }

  showGray(data, w=1) {
    var l = data.length;
    var size = Math.sqrt(l);
    size = Math.ceil(size);
    var img = new ImageData(size*w, size*w);
    for(var i=0; i<l;i++){
      var p = Math.floor(i/size);
      var q = i%size;

      for(var u=0; u<w; u++){
        for(var v=0; v<w; v++){
          var k = ((p*w+u)*w*size+(q*w+v))*4
          img.data[k] = data[i];
          img.data[k+1] = data[i];
          img.data[k+2] = data[i];
          img.data[k+3] = 255;
        }
      }
    }
    this.context.putImageData(img, 0, 0);
  }
}

class Pen {
  constructor(name, actions) {
    this.name = name;
    this.actions = actions;
    this.size = 0;
    this.x = 0;
    this.y = 0;
    this.isDrawing = false;
  }
}

class ToolButton {
  constructor(id, tool, painter) {
    this.id = id;
    this.tool = tool;
    this.painter = painter;
    $("#" + id).on("click", () => {
      this.painter.use(this.tool);
    });
  }
}

class Painter {
  constructor(){
    this.actions = [];
  }
  resetActions() {
    for (var action in this.actions) {
    }
  }
  use(newTool) {
    this.resetActions();
    this.tool = newTool;
  }
}



