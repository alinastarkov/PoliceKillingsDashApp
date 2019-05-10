/*
 Inc v1.0.0
 (c) 2014 Depth Development. http://depthdev.com
 License: Apache 2.0
*/

var number =  1

incrementNumber = setInterval(function(){
    if (number >= 467)  clearInterval(incrementNumber)
    else{
        var newNum = number +=1 
        document.getElementById('number').innerHTML = newNum
    }
}, 25)

