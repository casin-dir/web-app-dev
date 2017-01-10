function getMaxValue(array){
    var max = array[0];
    for (var i = 0; i < array.length; i++) {
        if (max < array[i]) max = array[i]; 
    }
    return max;
}
function getMinValue(array){
    var min = array[0];
    for (var i = 0; i < array.length; i++) {
        if (min > array[i]) min = array[i];
    }
    return min;
}

var Graph ={};

Graph.getValues = function(){
    this.values.from = parseFloat($('#point_from').val());
    this.values.to = parseFloat($('#point_to').val());
    this.values.function = $('#function').val();
}
Graph.createPointsArr = function(){
    this.getValues();

    var points = [];

    for (var x = this.values.from; x <= this.values.to; x += this.config.dx) {
        var new_twain = [];
        new_twain.push(x);
        new_twain.push(eval(this.config.prefix + this.values.function));
        points.push(new_twain);
    }

    return points;
}
Graph.addCurrentFunc = function(){
    var points = this.createPointsArr();
    var new_func = { label : this.values.function, data : points};
    this.func_arr.push(new_func);
}
Graph.displayFuncs = function(){

    $(this.config.target).plot(this.func_arr, this.config.options);
}
Graph.clear = function(){

    this.func_arr = [];
}
Graph.animate = function(){
    Graph.clear();
    Graph.displayFuncs();

    this.getValues();

    var func_vals = [];
    for (var x = this.values.from; x <= this.values.to; x += this.config.dx) {
        func_vals.push(eval(this.config.prefix + this.values.function));
    }

    var points = [];

    var x = this.values.from;
    var x_max = this.values.to;
    var dx = this.config.dx;
    var iter = 0;
    var y_max = getMaxValue(func_vals);
    var y_min = getMinValue(func_vals);

    var animateDraw = setInterval(function() {
        var obj = Graph;
      
        var new_twain = [];
        new_twain.push(x);
        new_twain.push(func_vals[iter]);
        points.push(new_twain);

        $(obj.config.target).plot(
            [ {label : obj.config.function, data : points} ],
            {   
                xaxis : {min : obj.values.from, max : obj.values.to}, 
                yaxis : {min: y_min, max: y_max}
            }
        );

        x += dx;
        iter++;

        if (x > x_max) {
            clearInterval(animateDraw);
        }
    }, this.config.delay);
}
Graph.init = function(){

    // current values
    this.values = {};
    this.values.from = 0;
    this.values.to = 0;
    this.values.function = '';

    // current fuctions
    this.func_arr = [];

    // std config
    this.config = {};
    this.config.target = $('#container_graph');
    this.config.dx = .1;
    this.config.options = {
        series: {
            lines: { show: true },
            points: { show: true }
        }
    };
    // this.config.prefix = 'Math.';
    this.config.prefix = '';
    this.config.delay = 1000/60;

    // event listeners
    $('#plot').click(function(){
        Graph.addCurrentFunc();
        Graph.displayFuncs();
    })
    $('#clear').click(function(){
        Graph.clear();
        Graph.displayFuncs();
    })
    $('#animate').click(function(){
        Graph.animate();
    })
}

$(document).ready(function() {

    // init
    Graph.init();
})

