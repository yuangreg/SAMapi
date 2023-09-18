// Initialization variables
let imageObj = new Image();
imageObj.src = document.getElementById('image').src;
imageObj.addEventListener("load" , setup_canvas , false);
let img_width = imageObj.width;
let img_height = imageObj.height;
const point_list = []
const label_list = []

let canvas = document.getElementById('canvas');
canvas.height = img_height;
canvas.width = img_width;
let ctx = canvas.getContext('2d');

// Function for drawing box
function draw_box(x, y, h, w){
  ctx.drawImage(imageObj, 0, 0);
  ctx.strokeStyle = 'red';
  ctx.strokeRect(x, y, h, w)
}

// Function to check whether point and label is valid
function check_point(){
  const pointInput = document.getElementById('point_input');
  const labelInput = document.getElementById('label_input');
  const regex1 = /^\d+,\d+$/;
  check1 = regex1.test(pointInput.value);
  const regex2 = /^\d+$/;
  check2 = regex2.test(labelInput.value) && (labelInput.value == 1 || labelInput.value == 0);
  if (check1 && check2)
    return true;
  else
    return false;
}

// Call back function to add a point
function add_point(){
  const pointInput = document.getElementById('point_input');
  const labelInput = document.getElementById('label_input');
  const pointList = document.getElementById('point_list');
  const labelList = document.getElementById('label_list');
  if(check_point()){
    const myArray = pointInput.value.split(",");
    const color = labelInput.value * 1;
    let x0= myArray[0] * 1;
    let y0= myArray[1] * 1;
    point_list.push([x0, y0]);
    label_list.push(color);
    pointInput.value = '';
    labelInput.value = '';
    pointList.value = point_list.join(',');
    labelList.value = label_list.join(',');
  }
}

// Setup canvas
function setup_canvas(){
  ctx.drawImage(imageObj, 0, 0);
  for (let i = 0; i < label_list.length; i++) {
    pos = point_list[i]
    color = label_list[i]
    draw_point(pos[0], pos[1], color)
  }
}

// Draw point function
function draw_point(x, y, ind){
  let color_palette = ['#6b5b95', '#feb236']
  let color = color_palette[ind]
  let size = 5;

  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.arc(x, y, size, 0 * Math.PI, 2 * Math.PI);
  ctx.fill();
}

// HTML display options
const modeSelect = document.getElementById('mode');
const inputFields = document.getElementById('input_fields');

modeSelect.addEventListener('change', function() {
    const mode = modeSelect.value;
    if (mode === 'box') {
      inputFields.innerHTML = '<label for="box_input">Enter 4 integers separated by comma:</label><br><input type="text" name="box_input" id="box_input">';
      const boxInput = document.getElementById('box_input');
      boxInput.addEventListener('input', function() {
        const regex = /^\d+,\d+,\d+,\d+$/;
        if (regex.test(boxInput.value)) {
          console.log('4 digits detected')
          const myArray = boxInput.value.split(",")
          let x0= myArray[0] * 1
          let y0= myArray[1] * 1
          let width = myArray[2]-x0
          let height = myArray[3]-y0
          draw_box(x0, y0, width, height)
        }
      });
    } else if (mode === 'text') {
      inputFields.innerHTML = '<label for="text_input">Enter some text:</label><br><input type="text" name="text_input" id="text_input">';
    } else if (mode === 'points') {
      inputFields.innerHTML = '<label for="point_input">Enter 2 integers separated by comma:</label><br><input type="text" name="point_input" id="point_input"><input type="hidden" name="point_list" id="point_list"><br><label for="label_input">Enter an integer:</label><br><input type="text" name="label_input" id="label_input"><input type="hidden" name="label_list" id="label_list"><button type="button" onclick="add_point()">Add point</button>';
      const pointInput = document.getElementById('point_input');
      const labelInput = document.getElementById('label_input');
      pointInput.addEventListener('input', function() {
        if (check_point()) {
          console.log('Requirement fulfilled')
          const myArray = pointInput.value.split(",")
          const color = labelInput.value * 1
          let x0= myArray[0] * 1
          let y0= myArray[1] * 1
          setup_canvas()
          draw_point(x0, y0, color)
        }
      });
      labelInput.addEventListener('input', function() {
        if (check_point()) {
          console.log('Requirement fulfilled')
          const myArray = pointInput.value.split(",")
          const color = labelInput.value * 1
          let x0= myArray[0] * 1
          let y0= myArray[1] * 1
          setup_canvas()
          draw_point(x0, y0, color)
        }
      });
    } else {
      inputFields.innerHTML = '';
    }
});




