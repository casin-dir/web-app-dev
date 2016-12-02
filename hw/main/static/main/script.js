var userMessage = {};
userMessage.show = function(text){
    var obj = this
    obj.html.css('display', 'flex');
    obj.html.find('#message_block').find('.message').text(text);
} 
userMessage.init = function(){
    var obj = this;
    obj.html = $('#user_message');
    obj.html.find('#message_block').find('.close').click(function(){
        obj.html.hide();
    })
}

var infinityList = {};
infinityList.updateGeneral = function(){
    var obj = this;
    obj.pageHeight = parseInt($(document).height());
    obj.winHeight = parseInt($(window).height());
}
infinityList.init = function(){
    var obj = this;

    obj.HTML_loading = $('#loading_block');
    obj.HTML_loading.hide();

    obj.footerHeight = $('footer').height();
    $('footer').hide();
    obj.updateGeneral();

    obj.scrollIndex = 0;
    obj.eror_lock = false;
    obj.load_lock = false;
    obj.end_of_list  = false;

    // ловим событие скрола
    $(document).scroll(function () { 
        var pos = parseInt($(document).scrollTop());

        if ((pos + obj.winHeight > obj.pageHeight - obj.footerHeight) &&  
            (!obj.load_lock) &&
            (!obj.end_of_list)) 
        {
            obj.HTML_loading.show();
            obj.scrollIndex++;
            console.log(obj.scrollIndex);
            obj.load_lock = true;
            $.ajax({
                url: '/page/' + obj.scrollIndex,
                type: 'GET',
                data: {},
                dataType: 'text',
                timeout: 60000,
                success: function(response){

                    console.log('response***' + response + '****');

                    if (response.trim() == 'N/A') {
                        obj.end_of_list = true;
                        $('footer').show();
                    }else{
                        obj.HTML_loading.before(response);
                    }

                    obj.HTML_loading.hide();
                    obj.updateGeneral();
                    obj.load_lock = false;
                },
                error: function(){
                    if (!obj.eror_lock) {
                        obj.scrollIndex--;
                        obj.eror_lock = true;
                        $(document).scrollTop(0);
                        alert('Упс... Что то пошло не так, обновите страницу и повторите попытку.');
                        setTimeout(function() { 
                            location.reload();
                        }, 1);
                    }
                }
            });
        }else{
            obj.HTML_loading.hide();
        }
    });

    // ресайз
    $(window).resize(function () {
        obj.updateGeneral();
    });
}

var modalWindow = {}
modalWindow.State = function(state){
    var obj = this;
    if (state == 'show') {
        obj.HTML.css('display', 'flex');
    }else{
        obj.HTML.css('display', 'none');
    }
}
modalWindow.init = function(){
    var obj = this;

    obj.maxImgSize = 1000000;

    obj.HTML = $('#modal_window');
    
    obj.State('hide');

    $('#show_modal_window').click(function(){
        
        obj.State('show');
    })

    $('#hide_modal_window').click(function(){
        
        obj.State('hide');
    })

    $('#new_rec_img').change(function(){

        var input = this;

        // выкачиваем данные из инпута
        if (input.files && input.files[0] && input.files[0].size <= obj.maxImgSize) {

            //  номальный файл
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#pre_img').css('background-image','url('+e.target.result+')');
                $('#pre_img').addClass('show');                
            }
            reader.readAsDataURL(input.files[0]);
        }else{
            userMessage.show('Максимальный размер файла: ' + obj.maxImgSize + ' байт');
            input.value = null;
            $('#pre_img').removeClass('show');
        }   
    })
}

function stickLeftBar(id){
    $('#' + id).unstick();
    $('#' + id).sticky({topSpacing: 70});
}

$('#add_rec_button').click(function(){

    var form = $('#form_add');

    var name = form.find('#new_rec_name').val(),
        country = form.find('#new_rec_country').val(),
        sport_type = form.find('#new_rec_sportType').val(),
        prize_count = parseInt(form.find('#new_rec_prizeCount').val()),
        desc = form.find('#new_rec_desc').val();

    if (name.length == 0) {
        userMessage.show('Введите имя команды.');      
        return;
    }

    if (country.length == 0) {
        userMessage.show('Введите страну команды.');      
        return;
    }

    if (sport_type.length == 0) {
        userMessage.show('Введите тип спорта.');      
        return;
    }

    if (isNaN(prize_count) || prize_count <= 0) {
        userMessage.show('Введите количество призов.');      
        return;
    }

    if (desc.length == 0) {
        userMessage.show('Введите описание команды.');      
        return;
    }

    var input = document.getElementById('new_rec_img');
    if (!input.files || !input.files[0] || input.files[0].size == 0) {
        userMessage.show('Добавьте картинку для команды.');      
        return;
    }

    form.submit();
})

$(document).ready(function () {
    infinityList.init();
    modalWindow.init();
    userMessage.init();
    stickLeftBar('left_bar_stick');
})

$(window).resize(function(){
    stickLeftBar('left_bar_stick');
})




    
