$(document).ready(function() {
  var passPatter = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/
  $("#al1").hide()
    console.log("ready");
    $("#cp1").keyup(function(){
      var pattern = new RegExp(/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d][A-Za-z\d!@#$%^&*()_+]{7,19}$/)
      var p1= $("#cp1").val()
      var t = pattern.test(p1)
      if(t==false){
        console.log(false)
        $("#cp1").text('Password contain atleast 1 uppercase, 1 lowercase and a special character').fadeIn(2000)
      }
    });
    $("#mdbtn").hide()
    //modalControl();
    //getAllImages();
    $( "#ralert" ).hide()
    
    $( "#lstart" ).click(function() {
      $(this).fadeOut(500)
      $("#maindiv").show(1000)
    });

    $( "#sregister" ).click(function() {
      var p1 = $( "#cp1" ).val()
      var p2 = $("#cp2").val()
      var pattern = new RegExp(/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d][A-Za-z\d!@#$%^&*()_+]{7,19}$/)
      var t = pattern.test(p1)
      if(t==false){
        $( "#ralert" ).text("Password contain atleast 1 uppercase, 1 lowercase and a special character").fadeIn(1000).fadeOut(4000);
        return false;
      }
      if(p1 == ""){
        $( "#ralert" ).text("Password Can not be Null").fadeIn(1000).fadeOut(4000);
        return false;
      }
      else if(!(p1 == p2)){
        $( "#ralert" ).text("Password Mismatch").fadeIn(1000).fadeOut(4000);
        //$( "#ralert" ).empty()
        return false;
      }
      else{
        return true;
      }
    });
    // function checkCount(){
    //   var numFiles = $("input:file", this)[0].files.length;
    //   console.log([11111,numFiles])
    //   return false;
    // }
    // function UserCreation(){
    //   var p1 = $( "#cp1" ).val()
    //   var p2 = $("#cp2").val()
    //   $.ajax({
    //     url : "/search2",
    //     type: "POST",
    //     data : formData,
    //     processData: false,
    //     contentType: false,
    //     success:function(data){
    //        console.log(data)
    //         displayResults(data)
    //         $("#mdbtn").click()
    //         $('#img1').hide();

    //     },
    //     error: function(error){
    //         console.log(error) 
    //         alert("Only formats are allowed : "+fileExtension.join(', '));  
    //         $('#img1').hide();
    //     }
    // });
    // }

    

    $( "#ldrr" ).click(function() {
      var imgVal = $('#image').val(); 
      var pathVal = $('#path').val(); 
        if(!(imgVal=='' && pathVal=='')) 
        {  
          $("#img1").show();
        } 
      
    });

    $( "#freset" ).click(function() {
      $("#path").prop('disabled', false);
      $('input[type=file]').prop('disabled', false);
      $("#forms").trigger("reset");
    });

    $('input[type=file]').change(function () {
      $("#path").prop('disabled', true);
      $("#freset").prop('disabled', false);
  });

  $('#path').change(function () {
    $('input[type=file]').prop('disabled', true);
    $("#freset").prop('disabled', false);
  });

    $("#forms22").submit(function (event) {
        event.preventDefault(); 
        
        var fileExtension = ['jpeg', 'jpg', 'png'];
        var formData = new FormData(this);
        formData.append('path', $('#path').val())
        formData.append('image',  $('#image')[0].files[0])
        formData.append('limit', $('#limit').val())
        formData.append('max', $('#max').val())
        console.log(formData)
        $('#img1').show();

        $.ajax({
            url : "/search2",
            type: "POST",
            data : formData,
            processData: false,
            contentType: false,
            success:function(data){
               console.log(data)
                displayResults(data)
                $("#mdbtn").click()
                $('#img1').hide();

            },
            error: function(error){
                console.log(error) 
                alert("Only formats are allowed : "+fileExtension.join(', '));  
                $('#img1').hide();
            }
        });
        return false; //<---- move it here
      });
  
  });

var displayResults = function(data){

    $("#results").html("");
    $("#ogimg").html("");
    var cls = "img-thumbnail float-start"
    try{
        var valid = data[0].valid
        if(valid==1){
            var og = data[0].ogimg;
            var imgelement = "<img src="+og+" class="+cls+">"
            $("#ogimg").append(imgelement);
            return
        }

    }
    catch{
        console.log('nope')
    }
    
    for(var i = 0; i < data.length; i++){
      var image = data[i].image;
      var score = data[i].score;
      var og = data[i].ogimg;
      var imgelement = "<img src="+og+" class="+cls+">"
      var element = "<div class= img-result ><img class=img-thumbnail src=static/dataset/"+image+"/>\
                     <div class=img-info>"+"<span class=image-name>IMAGE: "+image.split('.')[0]+"</span>\
                     <span class=img-score>SCORE: "+score+"</span></div></div>"
      $("#results").append(element);
    }
    $("#ogimg").append(imgelement);
  }


var displayModalImages = function(imgList){
  
    for(var i = 0; i < imgList.length; i++){
       $(".modal-images-list").append("<img src="+imgList[i].url+" class=modal-image onclick=imageSelectSearch(this,"+imgList[i].id+") />");
 
    }
 }


var getAllImages = function(){

    $.ajax({
     url: "/list",                   
     type: 'GET',
     success: function(data){
       //displayModalImages(data)
       console.log(data)
     },
     error: function(error){
       console.log(error);  
       
     }
  });
}