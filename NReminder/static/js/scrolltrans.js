$(function(){
    $('a').click(function(){
        //根据a标签的href转换为id选择器，获取id元素所处的位置，并高度减50px
        $('html,body').animate({scrollTop: ($($(this).attr('href')).offset().top -50 )},1000);
    });
});
