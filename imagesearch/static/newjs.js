function checkPage(){
    var start = 0;
    var nb = 15;
    var end = start + nb;
    var length = $('.res1 .res2').length;
    var totalpage = 0
    var currentpage = 1
    var ad = 0
    if(length==0){
        totalpage = 0
    }
    else{
        totalpage = Math.floor(length/nb)
        var mm = length/nb
        var nn = Math.floor(length/nb)
        if(mm==nn){
            console.log()
        }
        else{
            totalpage += 1 
        }
    }
    $("#crt").append(currentpage)
    $("#tot").append(totalpage)
    var list = $('.res1 .res2');
    list.hide().filter(':lt('+(end)+')').show();
    $('.prev, .next').click(function(e){
    e.preventDefault();

        if( $(this).hasClass('prev') ){
            if(start >= length){
                start -= 2*nb;
                currentpage -=1
                if(currentpage<1){
                    currentpage=1
                }
            $("#crt").empty()
            $("#crt").append(currentpage)
            }
            else{
                start -= nb;
            currentpage -=1
            if(currentpage<1){
                currentpage=1
            }
            $("#crt").empty()
            $("#crt").append(currentpage)
            }
        } else {
            // if(currentpage==totalpage){
            //     currentpage = 1
            // }
            if(start >= length){
                // console.log('stopped')
            }
            else{
            start += nb;
            currentpage +=1
            if(currentpage>totalpage){
                currentpage=totalpage
            }
            $("#crt").empty()
            $("#crt").append(currentpage)
            }
        }
        if(start >= length){
            // console.log('stopped')
        }
        else{
            if( start < 0) start = 0;
            end = start + nb; 
            if( start == 0 ){
                list.hide().filter(':lt('+(end)+')').show();
                } 
            else {
                list.hide().filter(':lt('+(end)+'):gt('+(start-1)+')').show();
            }
        }
        
    });
}

$("#imgresult").hide()
$("#formnew").submit(function(e){
    e.preventDefault()
    $("#imres").empty()
    $("#imgsearch").hide()
    $("#forloader").show()
    // console.log([CropData,12])
        var data = {}
        var formData = new FormData();
        var $image = $("#image");
        var cropData = CropData
        var x = cropData["x"]
        var y = cropData["y"]
        var ht = cropData["height"]
        var wd = cropData["width"]
        formData.append('path',$('#path').val())
        formData.append('image',  $('#id_image')[0].files[0])
        formData.append('limit', $('#limit').val())
        formData.append('max', $('#max').val())
        formData.append('x', x)
        formData.append('y', y)
        formData.append('height', ht)
        formData.append('width', wd)
        // for (var key of formData.entries()) {
		// 	console.log(key[0] + ', ' + key[1])
		// }
        var path = $('#path').val()
        var image = $('#id_image')[0].files[0]
        var limit = $('#limit').val()
        var max = $('#max').val()
        if (path){
            data['path'] = path
        }
        if (image){
            data['image'] = image
        }
        if (limit){
            data['limit'] = limit
        }
        if (max){
            data['path'] = max
        }

        $.ajax({
            url : "/search2",
            type: "POST",
            data : formData,
            processData: false,
            contentType: false,
            success:function(data){
                var primage = data.qimage
                var data = data.data
                
                
                for(var i = 0; i < data.length; i++){
                    var image = data[i].image;
                    var score = data[i].score;
                    var name = data[i].name;
                    var cl1 = "col-sm-12 col-md-6 col-lg-4 res1"
                    var element = "<div class='col-sm-12 col-md-6 col-lg-4 res1'><div class='card res2'><div class=card-body><img src="+image+" class=img-thumbnail></div>\
                        <div class=card-header><span>Name:<strong>"+name+"</strong></span><br><span>Score:<strong>"+score+"</strong> </span></div></div></div>"
                     $("#imres").append(element);
                  }
                  checkPage();
                  $("#primage").attr("src",primage);
                  $("#imgresult").show()
                  $("#forloader").hide()
            },
            error: function(error){
                console.log(error) 
            }
        });
});

$("#forsearch").click(function(){
    $("#crt").empty()
    $("#tot").empty()
    $("#imgsearch").show()
    $("#imgresult").hide()
})

$("#uptype").change(function(){
    $("#filed").val('')
    var val = $("#uptype").val()
    if(val==1){
        $("#filed").attr('webkitdirectory','false')
        $("#filed").attr('directory','false')
    }
    else{
        $("#filed").attr('webkitdirectory','true')
        $("#filed").attr('directory','true')
    }
})


// const alertBox = document.getElementById('alert-box')
// const imageBox = document.getElementById('image-box')
// const imageForm = document.getElementById('image-form')
// const confirmBtn = document.getElementById('confirm-btn')
// const input = document.getElementById('imageid')
// const csrf = document.getElementsByName('csrfmiddlewaretoken')
// $("#imageid").change(function(){
//     console.log(111)
//         alertBox.innerHTML = ""
//         confirmBtn.classList.remove('not-visible')
//         const img_data = input.files[0]
//         const url = URL.createObjectURL(img_data)
    
//         imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`
//         var $image = $('#image')
//         console.log($image)
    
//         $image.cropper({
//             aspectRatio: 16 / 9,
//             crop: function(event) {
//                 console.log(event.detail.x);
//                 console.log(event.detail.y);
//                 console.log(event.detail.width);
//                 console.log(event.detail.height);
//                 console.log(event.detail.rotate);
//                 console.log(event.detail.scaleX);
//                 console.log(event.detail.scaleY);
//             }
//         });
        
//         var cropper = $image.data('cropper');
//         confirmBtn.addEventListener('click', ()=>{
//             cropper.getCroppedCanvas().toBlob((blob) => {
//                 console.log('confirmed')
//                 const fd = new FormData();
//                 fd.append('csrfmiddlewaretoken', csrf[0].value)
//                 fd.append('file', blob, 'my-image.png');
    
//                 $.ajax({
//                     type:'POST',
//                     url: imageForm.action,
//                     enctype: 'multipart/form-data',
//                     data: fd,
//                     success: function(response){
//                         console.log('success', response)
//                         alertBox.innerHTML = `<div class="alert alert-success" role="alert">
//                                                 Successfully saved and cropped the selected image
//                                             </div>`
//                     },
//                     error: function(error){
//                         console.log('error', error)
//                         alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
//                                                 Ups...something went wrong
//                                             </div>`
//                     },
//                     cache: false,
//                     contentType: false,
//                     processData: false,
//                 })
//             })
//         })
//     })
