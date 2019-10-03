var paint = false;
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var canvasX = 0;
var canvasY = 0;
var canvasWidth = 280;
var canvasHeight = 280;

function initCanvas()
{
	// Create the canvas (Neccessary for IE because it doesn't know what a canvas element is)
	var canvasDiv = document.getElementById('canvasDiv');
	
	canvasX = canvasDiv.offsetLeft;
	canvasY = canvasDiv.offsetTop;
	
	canvas = document.createElement('canvas');
	canvas.setAttribute('width', canvasWidth);
	canvas.setAttribute('height', canvasHeight);
	canvas.setAttribute('id', 'canvas');
	canvasDiv.appendChild(canvas);
	if(typeof G_vmlCanvasManager != 'undefined') {
		canvas = G_vmlCanvasManager.initElement(canvas);
	}
	context = canvas.getContext("2d"); // Grab the 2d canvas context
	// Note: The above code is a workaround for IE 8 and lower. Otherwise we could have used:
	//     context = document.getElementById('canvas').getContext("2d");
	

	// Add mouse events
	// ----------------
	$('#canvas').mousedown(function(e)
	{
		// Mouse down location
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
		
		paint = true;
		addClick(mouseX, mouseY, false);
		redraw();
	});
	
	$('#canvas').mousemove(function(e){
		if(paint==true){
			addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
			redraw();
		}
	});
	
	$('#canvas').mouseup(function(e){
		paint = false;
	  	redraw();
	});
	
	$('#canvas').mouseleave(function(e){
		paint = false;
	});
}

/**
* Adds a point to the drawing array.
* @param x
* @param y
* @param dragging
*/
function addClick(x, y, dragging)
{
	clickX.push(x);
	clickY.push(y);
	clickDrag.push(dragging);
}

function clearCanvas()
{
	context.clearRect(canvasX, canvasY, canvasWidth, canvasHeight);
}

function redraw()
{
	clearCanvas();
		
	context.strokeStyle = 'white';
	context.lineJoin = "round";
	context.lineWidth = 30;
	
	var i = 0;
	for(; i < clickX.length; i++)
	{		
		context.beginPath();
		if(clickDrag[i] && i){
			context.moveTo(clickX[i-1], clickY[i-1]);
		}else{
			context.moveTo(clickX[i], clickY[i]);
		}
		context.lineTo(clickX[i], clickY[i]);
		context.closePath();
		context.stroke();
		
	}
}

function getData(){
	var imgd = context.getImageData(canvasX, canvasY, canvasWidth, canvasHeight);
	var pixels = imgd.data;
	
	var gray = new Array(canvasWidth);
	for (var i = 0; i < canvasWidth; i++)
	  gray[i] = new Array(canvasHeight);
	
	for (i = 0; i < pixels.length; i += 4) {
		x = ((i/4)%canvasWidth);
		y = Math.floor((i/(4*canvasWidth)));
		gray[y][x] = Math.floor((pixels[i]+pixels[i+1]+pixels[i+2])/3)
    }
	return gray;
}
	
function predict(url){

	var gray = getData();
	$.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify({data:gray}),
        dataType: "text",
        processData: false,
        contentType: false,
        success: function(response) {
            $('#prediction')[0].value = response
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        }
    });
}